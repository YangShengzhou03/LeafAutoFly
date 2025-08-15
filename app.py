from flask import Flask, render_template, request, jsonify
import uuid
import datetime
import json
import os

app = Flask(__name__)

# 后端数据存储 - 使用字典存储任务
# 格式: {task_id: task_data}
tasks = {}

# 数据持久化 - 使用JSON文件
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.json')

# 加载任务数据
def load_tasks():
    global tasks
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                tasks = json.load(f)
    except Exception as e:
        print(f'加载任务数据失败: {e}')
        tasks = {}

# 保存任务数据
def save_tasks():
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f'保存任务数据失败: {e}')

# 初始化加载任务
load_tasks()

# 确保tasks字典只被定义一次
# 初始化加载任务已在前面完成

# 主页路由
@app.route('/')
def home():
    return render_template('home.html')

# 自动信息页面路由
@app.route('/auto-info')
def auto_info():
    return render_template('auto_info.html')

# AI接管页面路由
@app.route('/ai-takeover')
def ai_takeover():
    return render_template('ai_takeover.html')

# API接口: 获取所有任务
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    # 转换为列表返回
    return jsonify(list(tasks.values()))

# API接口: 添加新任务
@app.route('/api/tasks', methods=['POST'])
def add_task():
    task_data = request.json
    # 生成唯一ID
    task_id = str(uuid.uuid4())
    # 添加创建时间
    task_data['id'] = task_id
    task_data['createdAt'] = datetime.datetime.now().isoformat()
    # 保存到字典
    tasks[task_id] = task_data
    # 保存到文件
    save_tasks()
    return jsonify(task_data), 201

# API接口: 删除任务
@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    if task_id in tasks:
        del tasks[task_id]
        # 保存到文件
        save_tasks()
        return jsonify({'success': True}), 200
    return jsonify({'error': 'Task not found'}), 404

# API接口: 更新任务状态
@app.route('/api/tasks/<task_id>/status', methods=['PATCH'])
def update_task_status(task_id):
    if task_id not in tasks:
        return jsonify({'error': 'Task not found'}), 404
    
    data = request.json
    if 'status' not in data:
        return jsonify({'error': 'Status field is required'}), 400
    
    # 更新任务状态
    tasks[task_id]['status'] = data['status']
    tasks[task_id]['updatedAt'] = datetime.datetime.now().isoformat()
    
    # 保存到文件
    save_tasks()
    
    return jsonify(tasks[task_id]), 200

# API接口: 清空所有任务
@app.route('/api/tasks', methods=['DELETE'])
def clear_tasks():
    tasks.clear()
    # 保存到文件
    save_tasks()
    return jsonify({'success': True}), 200

if __name__ == '__main__':
    app.run(debug=True)
