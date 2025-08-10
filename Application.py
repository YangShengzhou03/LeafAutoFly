import os
import json
import time
import random
import datetime
from flask import Flask, request, jsonify, render_template, send_from_directory
import threading

app = Flask(__name__, static_folder='.', static_url_path='')

# 模拟数据库 - 实际应用中应使用真实数据库
TASKS = []
ACTIVITIES = []
RULES = []
NEXT_TASK_ID = 1
NEXT_ACTIVITY_ID = 1

# 模拟微信实例
WECHAT_INSTANCES = [
    {"id": 1, "name": "当前微信", "status": "已连接", "last_active": datetime.datetime.now().isoformat()}
]

# 模拟AI状态
AI_STATUS = {
    "running": False,
    "start_time": None,
    "processed_count": 0,
    "ai_reply_count": 0,
    "rule_reply_count": 0,
    "settings": {
        "receiver": "",
        "global_takeover": False,
        "model": "moonshot",
        "role": "",
        "only_at": False
    }
}


# 任务执行线程
class TaskExecutor(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.running = True
        self.paused = False

    def run(self):
        while self.running:
            if not self.paused:
                now = datetime.datetime.now()
                # 检查并执行到期任务
                for task in TASKS:
                    if task["status"] == "pending":
                        task_time = datetime.datetime.fromisoformat(task["time"])
                        if now >= task_time:
                            self.execute_task(task)

            time.sleep(1)  # 每秒检查一次

    def execute_task(self, task):
        # 模拟执行任务
        success = random.random() > 0.2  # 80%成功率
        task["status"] = "completed" if success else "failed"
        task["last_executed"] = datetime.datetime.now().isoformat()

        # 记录活动
        add_activity(
            "发送消息" if success else "发送失败",
            f"向 {task['receiver']} 发送消息: {task['message']}",
            "success" if success else "error"
        )

        # 处理重复任务
        if task["frequency"] != "once" and success:
            task["status"] = "pending"
            # 更新下次执行时间
            task_time = datetime.datetime.fromisoformat(task["time"])
            if task["frequency"] == "daily":
                next_time = task_time + datetime.timedelta(days=1)
            elif task["frequency"] == "workdays":
                days = 1
                while True:
                    next_day = task_time + datetime.timedelta(days=days)
                    if next_day.weekday() < 5:  # 周一到周五
                        break
                    days += 1
                next_time = next_day
            elif task["frequency"] == "weekends":
                days = 1
                while True:
                    next_day = task_time + datetime.timedelta(days=days)
                    if next_day.weekday() >= 5:  # 周六和周日
                        break
                    days += 1
                next_time = next_day
            else:  # custom，这里简单处理为每天
                next_time = task_time + datetime.timedelta(days=1)

            task["time"] = next_time.isoformat()

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def stop(self):
        self.running = False


# 启动任务执行器
task_executor = TaskExecutor()
task_executor.start()


# 辅助函数：添加活动记录
def add_activity(activity_type, content, status):
    global NEXT_ACTIVITY_ID
    activity = {
        "id": NEXT_ACTIVITY_ID,
        "time": datetime.datetime.now().isoformat(),
        "type": activity_type,
        "content": content,
        "status": status
    }
    ACTIVITIES.append(activity)
    NEXT_ACTIVITY_ID += 1
    # 限制活动记录数量
    if len(ACTIVITIES) > 1000:
        ACTIVITIES.pop(0)
    return activity


# 路由：首页 - 提供前端页面
@app.route('/')
def index():
    # 尝试多种方式返回首页，增加容错性
    try:
        # 尝试从模板目录加载
        return render_template('index.html')
    except:
        try:
            # 尝试从静态目录加载
            return send_from_directory(app.static_folder, 'index.html')
        except:
            # 如果都失败，返回简单的提示信息
            return "服务器运行中，但未找到首页文件(index.html)", 200


# 路由：获取所有任务
@app.route('/api/get_tasks', methods=['GET'])
def get_tasks():
    return jsonify(TASKS)


# 路由：添加新任务
@app.route('/api/add_task', methods=['POST'])
def add_task():
    global NEXT_TASK_ID
    data = request.json

    # 验证必要字段
    if not all(k in data for k in ['receiver', 'message', 'time', 'frequency']):
        return jsonify({"status": "error", "message": "缺少必要字段"})

    task = {
        "id": NEXT_TASK_ID,
        "receiver": data['receiver'],
        "message": data['message'],
        "time": data['time'],
        "frequency": data['frequency'],
        "status": "pending",
        "created_at": datetime.datetime.now().isoformat(),
        "last_executed": None
    }

    TASKS.append(task)
    NEXT_TASK_ID += 1

    # 记录活动
    add_activity("添加任务", f"新增任务: 向 {task['receiver']} 发送消息", "success")

    return jsonify({"status": "success", "task_id": task["id"]})


# 路由：更新任务
@app.route('/api/update_task', methods=['POST'])
def update_task():
    data = request.json

    # 查找任务
    task = next((t for t in TASKS if t["id"] == data.get('id')), None)
    if not task:
        return jsonify({"status": "error", "message": "任务不存在"})

    # 更新任务字段
    if 'receiver' in data:
        task['receiver'] = data['receiver']
    if 'message' in data:
        task['message'] = data['message']
    if 'time' in data:
        task['time'] = data['time']
    if 'frequency' in data:
        task['frequency'] = data['frequency']

    # 记录活动
    add_activity("更新任务", f"更新任务 #{task['id']}", "success")

    return jsonify({"status": "success"})


# 路由：删除任务
@app.route('/api/remove_task', methods=['POST'])
def remove_task():
    data = request.json
    task_id = data.get('id')

    global TASKS
    # 查找并删除任务
    task = next((t for t in TASKS if t["id"] == task_id), None)
    if not task:
        return jsonify({"status": "error", "message": "任务不存在"})

    TASKS = [t for t in TASKS if t["id"] != task_id]

    # 记录活动
    add_activity("删除任务", f"删除任务 #{task_id}", "success")

    return jsonify({"status": "success"})


# 路由：启动任务
@app.route('/api/start_task', methods=['POST'])
def start_task():
    data = request.json
    task_id = data.get('id')
    start_all = data.get('all', False)

    if start_all:
        # 启动所有任务
        for task in TASKS:
            task["status"] = "pending"
        task_executor.resume()
        add_activity("启动任务", "启动所有任务", "success")
        return jsonify({"status": "success"})
    elif task_id:
        # 启动单个任务
        task = next((t for t in TASKS if t["id"] == task_id), None)
        if not task:
            return jsonify({"status": "error", "message": "任务不存在"})

        task["status"] = "pending"
        add_activity("启动任务", f"启动任务 #{task_id}", "success")
        return jsonify({"status": "success"})

    return jsonify({"status": "error", "message": "参数错误"})


# 路由：停止任务
@app.route('/api/stop_task', methods=['POST'])
def stop_task():
    data = request.json
    task_id = data.get('id')
    stop_all = data.get('all', False)

    if stop_all:
        # 停止所有任务
        for task in TASKS:
            if task["status"] == "pending":
                task["status"] = "stopped"
        task_executor.pause()
        add_activity("停止任务", "停止所有任务", "success")
        return jsonify({"status": "success"})
    elif task_id:
        # 停止单个任务
        task = next((t for t in TASKS if t["id"] == task_id), None)
        if not task:
            return jsonify({"status": "error", "message": "任务不存在"})

        if task["status"] == "pending":
            task["status"] = "stopped"
        add_activity("停止任务", f"停止任务 #{task_id}", "success")
        return jsonify({"status": "success"})

    return jsonify({"status": "error", "message": "参数错误"})


# 路由：刷新微信
@app.route('/api/reload_wx', methods=['POST'])
def reload_wx():
    # 模拟刷新微信
    for instance in WECHAT_INSTANCES:
        instance["status"] = "连接中"
        instance["last_active"] = datetime.datetime.now().isoformat()

    # 模拟延迟
    time.sleep(1)

    for instance in WECHAT_INSTANCES:
        instance["status"] = "已连接"

    add_activity("系统操作", "刷新微信实例", "success")
    return jsonify({
        "status": "success",
        "message": "微信已成功刷新",
        "instances": WECHAT_INSTANCES
    })


# 路由：检查更新
@app.route('/api/check_update', methods=['GET'])
def check_update():
    # 模拟检查更新
    return jsonify({
        "status": "success",
        "is_latest": True,
        "current_version": "v1.0.0",
        "latest_version": "v1.0.0"
    })


# 路由：获取AI状态
@app.route('/api/get_ai_status', methods=['GET'])
def get_ai_status():
    return jsonify(AI_STATUS)


# 路由：更新AI设置
@app.route('/api/update_ai_settings', methods=['POST'])
def update_ai_settings():
    data = request.json
    AI_STATUS["settings"].update(data)
    add_activity("系统操作", "更新AI设置", "success")
    return jsonify({"status": "success"})


# 路由：切换AI状态
@app.route('/api/toggle_ai', methods=['POST'])
def toggle_ai():
    data = request.json
    enable = data.get('enable', False)

    if enable and not AI_STATUS["running"]:
        AI_STATUS["running"] = True
        AI_STATUS["start_time"] = datetime.datetime.now().isoformat()
        add_activity("AI操作", "启动AI接管", "success")
    elif not enable and AI_STATUS["running"]:
        AI_STATUS["running"] = False
        add_activity("AI操作", "停止AI接管", "success")

    return jsonify({"status": "success", "running": AI_STATUS["running"]})


# 路由：获取活动记录
@app.route('/api/get_activities', methods=['GET'])
def get_activities():
    # 按时间倒序返回
    return jsonify(sorted(ACTIVITIES, key=lambda x: x["time"], reverse=True))


# 路由：清空活动记录
@app.route('/api/clear_activities', methods=['POST'])
def clear_activities():
    global ACTIVITIES
    ACTIVITIES = []
    add_activity("系统操作", "清空活动记录", "success")
    return jsonify({"status": "success"})


# 路由：获取规则
@app.route('/api/get_rules', methods=['GET'])
def get_rules():
    return jsonify(RULES)


# 路由：添加规则
@app.route('/api/add_rule', methods=['POST'])
def add_rule():
    data = request.json
    rule = {
        "id": len(RULES) + 1,
        "keyword": data.get('keyword', ''),
        "match_type": data.get('match_type', '包含'),
        "reply_content": data.get('reply_content', ''),
        "apply_to": data.get('apply_to', '全部')
    }
    RULES.append(rule)
    add_activity("系统操作", f"添加AI规则: {rule['keyword']}", "success")
    return jsonify({"status": "success", "rule": rule})


# 路由：删除规则
@app.route('/api/remove_rule', methods=['POST'])
def remove_rule():
    data = request.json
    rule_id = data.get('id')
    global RULES
    RULES = [r for r in RULES if r["id"] != rule_id]
    add_activity("系统操作", f"删除AI规则 #{rule_id}", "success")
    return jsonify({"status": "success"})


# 启动应用
if __name__ == '__main__':
    # 添加一些测试数据
    if not TASKS:
        test_time = (datetime.datetime.now() + datetime.timedelta(minutes=10)).isoformat()[:16]
        TASKS.append({
            "id": NEXT_TASK_ID,
            "receiver": "测试好友",
            "message": "这是一条测试消息",
            "time": test_time,
            "frequency": "once",
            "status": "pending",
            "created_at": datetime.datetime.now().isoformat(),
            "last_executed": None
        })
        NEXT_TASK_ID += 1

    app.run(debug=True, host='0.0.0.0', port=5000)
