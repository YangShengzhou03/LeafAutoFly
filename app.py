from flask import Flask, render_template, request, jsonify
import uuid
import datetime

app = Flask(__name__)

# 后端数据存储 - 使用字典存储任务
# 格式: {task_id: task_data}
tasks = {}

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
    return jsonify(task_data), 201

# API接口: 删除任务
@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    if task_id in tasks:
        del tasks[task_id]
        return jsonify({'success': True}), 200
    return jsonify({'error': 'Task not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
