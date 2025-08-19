from flask import Flask, request, jsonify, redirect
from data_manager import (
    load_tasks, save_tasks, load_ai_data, save_ai_data,
    add_task, delete_task, update_task_status, clear_tasks,
    save_ai_settings, add_ai_history, tasks, ai_settings, reply_history
)
from server_manager import start_vue_server, open_browser

# 初始化数据
app = Flask(__name__)

# 初始化数据
load_tasks()
load_ai_data()

@app.route('/')
def home():
    return redirect('http://localhost:8080')

@app.route('/auto-info')
def auto_info():
    return redirect('http://localhost:8080/auto_info')

@app.route('/ai-takeover')
def ai_takeover():
    return redirect('http://localhost:8080/ai_takeover')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(list(tasks.values()))

@app.route('/api/tasks', methods=['POST'])
def add_task_route():
    task_data = request.json
    new_task = add_task(task_data)
    return jsonify(new_task), 201

@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task_route(task_id):
    success = delete_task(task_id)
    if success:
        return jsonify({'success': True}), 200
    return jsonify({'error': 'Task not found'}), 404

@app.route('/api/tasks/<task_id>/status', methods=['PATCH'])
def update_task_status_route(task_id):
    data = request.json
    if 'status' not in data:
        return jsonify({'error': 'Status field is required'}), 400
    
    updated_task = update_task_status(task_id, data['status'])
    if updated_task:
        return jsonify(updated_task), 200
    return jsonify({'error': 'Task not found'}), 404

@app.route('/api/tasks', methods=['DELETE'])
def clear_tasks_route():
    clear_tasks()
    return jsonify({'success': True}), 200


@app.route('/api/ai-settings', methods=['POST'])
def save_ai_settings_route():
    settings_data = request.json
    saved_settings = save_ai_settings(settings_data)
    return jsonify(saved_settings), 200


@app.route('/api/ai-history', methods=['GET'])
def get_ai_history():
    return jsonify(reply_history)


@app.route('/api/ai-history', methods=['POST'])
def add_ai_history_route():
    history_data = request.json
    new_history = add_ai_history(history_data)
    return jsonify(new_history), 201



if __name__ == '__main__':
    # 注意：单独运行app.py只会启动Flask后端服务器
    # 若要同时启动前后端，请使用start_app.py脚本
    print('正在启动Flask后端服务器...')
    app.run(debug=True)
