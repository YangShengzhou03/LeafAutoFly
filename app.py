from flask import Flask, request, jsonify, redirect
import uuid
import datetime
import json
import os
import subprocess
import platform
import time

app = Flask(__name__)

tasks = {}
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.json')

aio_settings = {}
AI_DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ai_data.json')
reply_history = []

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


def load_ai_data():
    global ai_settings, reply_history
    try:
        if os.path.exists(AI_DATA_FILE):
            with open(AI_DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                ai_settings = data.get('settings', {})
                reply_history = data.get('history', [])
    except Exception as e:
        print(f'加载AI数据失败: {e}')
        ai_settings = {}
        reply_history = []


def save_ai_data():
    try:
        data = {
            'settings': ai_settings,
            'history': reply_history
        }
        with open(AI_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f'保存AI数据失败: {e}')


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


@app.route('/api/ai-settings', methods=['POST'])
def save_ai_settings():
    global ai_settings
    settings_data = request.json
    ai_settings = settings_data
    ai_settings['updatedAt'] = datetime.datetime.now().isoformat()
    save_ai_data()
    return jsonify(ai_settings), 200


@app.route('/api/ai-history', methods=['GET'])
def get_ai_history():
    return jsonify(reply_history)


@app.route('/api/ai-history', methods=['POST'])
def add_ai_history():
    global reply_history
    history_data = request.json
    history_data['id'] = str(uuid.uuid4())
    history_data['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    reply_history.append(history_data)
    save_ai_data()
    return jsonify(history_data), 201

def is_vue_server_running():
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 8080))
        sock.close()
        return result == 0
    except Exception:
        return False

def start_vue_server():
    try:
        if is_vue_server_running():
            print('Vue开发服务器已经在运行')
            return
        
        print('正在启动Vue开发服务器...')
        
        if platform.system() == 'Windows':
            cmd = 'npm run serve'
            process = subprocess.Popen(
                cmd,
                cwd=os.path.dirname(os.path.abspath(__file__)),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True
            )
        else:
            cmd = ['npm', 'run', 'serve']
            process = subprocess.Popen(
                cmd,
                cwd=os.path.dirname(os.path.abspath(__file__)),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=False
            )
        
        stdout, stderr = process.communicate()
        print(f'Vue服务器输出: {stdout.decode() if stdout else "无"}')
        if stderr:
            print(f'Vue服务器错误: {stderr.decode()}')
            
        print('Vue开发服务器已启动')
        time.sleep(3)
    except Exception as e:
        print(f'启动Vue开发服务器失败: {e}')

def open_browser():
    try:
        import webbrowser
        print('正在打开浏览器...')
        webbrowser.open('http://localhost:8080')
    except Exception as e:
        print(f'打开浏览器失败: {e}')

if __name__ == '__main__':
    start_vue_server()
    open_browser()
    app.run(debug=True, port=5000)
