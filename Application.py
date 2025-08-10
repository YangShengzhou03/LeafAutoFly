import json
import os
import threading
import time
from datetime import datetime, timedelta
import logging
from flask import Flask, render_template, request, jsonify
from wxauto import WeChat

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('wechat_scheduler.log'),
        logging.StreamHandler()
    ]
)

# 初始化微信
try:
    wx = WeChat()
    logging.info("微信初始化成功")
except Exception as e:
    logging.error(f"微信初始化失败: {str(e)}")
    wx = None

app = Flask(__name__)

# 内存存储任务列表
tasks = []
task_id_counter = 1

# 数据持久化到本地文件
DATA_FILE = "tasks.json"
# 存储活跃的任务线程
task_threads = {}


def load_tasks():
    """从本地文件加载任务"""
    global tasks, task_id_counter
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                tasks = json.load(f)
                if tasks:
                    task_id_counter = max(task['id'] for task in tasks) + 1
                    logging.info(f"成功加载 {len(tasks)} 个任务")

                    # 重启未完成的任务
                    for task in tasks:
                        if task['status'] == 'pending':
                            start_task_worker(task['id'])
        except Exception as e:
            logging.error(f"加载任务失败: {str(e)}")
            tasks = []


def save_tasks():
    """保存任务到本地文件"""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
        logging.info(f"已保存 {len(tasks)} 个任务")
    except Exception as e:
        logging.error(f"保存任务失败: {str(e)}")


def send_wechat_message(who, msg):
    """发送微信消息并处理异常"""
    if not wx:
        logging.error("微信未初始化，无法发送消息")
        return False

    try:
        wx.SendMsg(msg=msg, who=who)
        logging.info(f"已向 {who} 发送消息: {msg}")
        return True
    except Exception as e:
        logging.error(f"发送消息给 {who} 失败: {str(e)}")
        return False


def calculate_next_run_time(task):
    """计算任务的下一次运行时间"""
    current_time = datetime.now()
    last_run_time = datetime.fromisoformat(task['last_run']) \
        if 'last_run' in task else datetime.fromisoformat(task['time'])

    frequency = task['frequency'][0] if task['frequency'] else '仅一次'

    if frequency == '仅一次':
        return None
    elif frequency == '每天':
        return last_run_time + timedelta(days=1)
    elif frequency == '每周':
        return last_run_time + timedelta(weeks=1)
    elif frequency == '每月':
        # 简化处理，实际可能需要更复杂的逻辑
        return last_run_time + timedelta(days=30)
    return None


def task_worker(task_id):
    """任务执行线程，支持重复执行"""
    global tasks
    logging.info(f"任务线程 {task_id} 启动")

    try:
        while True:
            # 查找任务
            task = next((t for t in tasks if t['id'] == task_id), None)
            if not task:
                logging.info(f"任务 {task_id} 不存在，线程退出")
                break

            # 检查任务状态
            if task['status'] != 'pending':
                logging.info(f"任务 {task_id} 状态为 {task['status']}，线程退出")
                break

            # 检查任务是否需要执行
            now = datetime.now()
            task_time = datetime.fromisoformat(task['time'])

            if now >= task_time:
                # 执行任务：发送微信消息
                success = send_wechat_message(task['name'], task['info'])

                # 更新任务信息
                task['last_run'] = now.isoformat()
                task['last_status'] = '成功' if success else '失败'

                # 计算下一次运行时间（如果需要）
                next_time = calculate_next_run_time(task)
                if next_time:
                    task['time'] = next_time.isoformat()
                    logging.info(f"任务 {task_id} 将在 {task['time']} 再次执行")
                else:
                    task['status'] = 'completed'
                    logging.info(f"任务 {task_id} 已完成")

                save_tasks()

                # 如果是一次性任务，执行后退出
                if not next_time:
                    break

            # 每10秒检查一次
            time.sleep(10)

    except Exception as e:
        logging.error(f"任务线程 {task_id} 出错: {str(e)}")
    finally:
        if task_id in task_threads:
            del task_threads[task_id]
        logging.info(f"任务线程 {task_id} 已停止")


def start_task_worker(task_id):
    """启动任务线程并跟踪"""
    if task_id in task_threads and task_threads[task_id].is_alive():
        logging.warning(f"任务 {task_id} 线程已存在，无需重复启动")
        return False

    thread = threading.Thread(target=task_worker, args=(task_id,), daemon=True)
    task_threads[task_id] = thread
    thread.start()
    logging.info(f"已启动任务 {task_id} 的执行线程")
    return True


@app.route('/')
def index():
    """首页"""
    return render_template('index.html')


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """获取所有任务"""
    return jsonify(tasks)


@app.route('/api/tasks', methods=['POST'])
def create_task():
    """创建新任务"""
    global tasks, task_id_counter
    data = request.json

    # 验证必要参数
    required_fields = ['time', 'name', 'info']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "缺少必要参数"}), 400

    # 验证时间格式
    try:
        task_time = datetime.fromisoformat(data['time'])
        if task_time < datetime.now():
            return jsonify({"error": "任务时间不能早于当前时间"}), 400
    except ValueError:
        return jsonify({"error": "时间格式不正确，应为ISO格式 (YYYY-MM-DDTHH:MM:SS)"}), 400

    # 验证频率参数
    valid_frequencies = ['仅一次', '每天', '每周', '每月']
    frequency = data.get('frequency', ['仅一次'])
    if not isinstance(frequency, list) or len(frequency) == 0 or frequency[0] not in valid_frequencies:
        return jsonify({"error": f"频率参数无效，必须是 {valid_frequencies} 中的一个"}), 400

    # 创建新任务
    task = {
        'id': task_id_counter,
        'time': data['time'],
        'name': data['name'],
        'info': data['info'],
        'frequency': frequency,
        'status': 'pending',
        'created_at': datetime.now().isoformat(),
        'last_run': None,
        'last_status': None
    }

    tasks.append(task)
    task_id_counter += 1
    save_tasks()

    # 启动任务线程
    start_task_worker(task['id'])

    return jsonify(task), 201


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """删除任务"""
    global tasks
    initial_length = len(tasks)
    tasks = [t for t in tasks if t['id'] != task_id]

    if len(tasks) < initial_length:
        # 停止相关线程
        if task_id in task_threads:
            # 标记任务为已取消
            for task in tasks:
                if task['id'] == task_id:
                    task['status'] = 'cancelled'
                    break
            save_tasks()
            logging.info(f"任务 {task_id} 已取消")

        save_tasks()
        return jsonify({"success": True})
    return jsonify({"error": "任务不存在"}), 404


@app.route('/api/tasks/<int:task_id>/status', methods=['GET'])
def get_task_status(task_id):
    """获取任务状态"""
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task:
        return jsonify({
            'id': task['id'],
            'status': task['status'],
            'last_run': task.get('last_run'),
            'last_status': task.get('last_status'),
            'next_run': task['time'] if task['status'] == 'pending' else None
        })
    return jsonify({"error": "任务不存在"}), 404


@app.route('/api/tasks/<int:task_id>/status', methods=['PUT'])
def update_task_status(task_id):
    """更新任务状态（暂停/恢复）"""
    data = request.json
    if 'status' not in data or data['status'] not in ['pending', 'paused']:
        return jsonify({"error": "状态参数无效，必须是 'pending' 或 'paused'"}), 400

    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return jsonify({"error": "任务不存在"}), 404

    # 如果从暂停状态恢复，需要重新启动线程
    if data['status'] == 'pending' and task['status'] == 'paused':
        task['status'] = 'pending'
        start_task_worker(task_id)
    else:
        task['status'] = data['status']

    save_tasks()
    return jsonify({"success": True, "status": task['status']})


if __name__ == '__main__':
    # 启动时加载任务
    load_tasks()
    # 禁用debug模式以在生产环境中使用
    app.run(host='0.0.0.0', port=5000, debug=False)
