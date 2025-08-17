from flask import Flask, render_template, request, jsonify
import uuid
import datetime
import json
import os

app = Flask(__name__)

tasks = {}
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.json')

def load_tasks():
    global tasks
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                tasks = json.load(f)
    except Exception as e:
        print(f'加载任务数据失败: {e}')
        tasks = {}

def save_tasks():
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f'保存任务数据失败: {e}')

load_tasks()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/auto-info')
def auto_info():
    return render_template('auto_info.html')

@app.route('/ai-takeover')
def ai_takeover():
    return render_template('ai_takeover.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(list(tasks.values()))

@app.route('/api/tasks', methods=['POST'])
def add_task():
    task_data = request.json
    task_id = str(uuid.uuid4())
    task_data['id'] = task_id
    task_data['createdAt'] = datetime.datetime.now().isoformat()
    tasks[task_id] = task_data
    save_tasks()
    return jsonify(task_data), 201

@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    if task_id in tasks:
        del tasks[task_id]
        save_tasks()
        return jsonify({'success': True}), 200
    return jsonify({'error': 'Task not found'}), 404

@app.route('/api/tasks/<task_id>/status', methods=['PATCH'])
def update_task_status(task_id):
    if task_id not in tasks:
        return jsonify({'error': 'Task not found'}), 404
    
    data = request.json
    if 'status' not in data:
        return jsonify({'error': 'Status field is required'}), 400
    
    tasks[task_id]['status'] = data['status']
    tasks[task_id]['updatedAt'] = datetime.datetime.now().isoformat()
    save_tasks()
    
    return jsonify(tasks[task_id]), 200

@app.route('/api/tasks', methods=['DELETE'])
def clear_tasks():
    tasks.clear()
    save_tasks()
    return jsonify({'success': True}), 200

if __name__ == '__main__':
    app.run(debug=True)
