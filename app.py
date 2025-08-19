from flask import Flask, render_template, request, jsonify, redirect
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

def is_vue_server_running():
    """检查Vue开发服务器是否已经在运行"""
    try:
        # 尝试连接到Vue服务器
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 8080))
        sock.close()
        return result == 0
    except Exception:
        return False

def start_vue_server():
    try:
        # 检查Vue服务器是否已经在运行
        if is_vue_server_running():
            print('Vue开发服务器已经在运行')
            return
        
        print('正在启动Vue开发服务器...')
        
        # 根据操作系统设置正确的命令格式
        if platform.system() == 'Windows':
            # 在Windows上使用shell=True时，命令应该是字符串
            cmd = 'npm run serve'
            # 不使用列表形式，因为shell=True会在cmd.exe中执行
            process = subprocess.Popen(
                cmd,
                cwd=os.path.dirname(os.path.abspath(__file__)),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True
            )
        else:
            # 在非Windows系统上，可以使用列表形式
            cmd = ['npm', 'run', 'serve']
            process = subprocess.Popen(
                cmd,
                cwd=os.path.dirname(os.path.abspath(__file__)),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=False
            )
        
        # 输出命令执行的信息
        stdout, stderr = process.communicate()
        print(f'Vue服务器输出: {stdout.decode() if stdout else "无"}')
        if stderr:
            print(f'Vue服务器错误: {stderr.decode()}')
            
        print('Vue开发服务器已启动')
        # 等待Vue服务器启动完成
        time.sleep(3)
    except Exception as e:
        print(f'启动Vue开发服务器失败: {e}')

def open_browser():
    # 自动打开浏览器
    try:
        import webbrowser
        print('正在打开浏览器...')
        webbrowser.open('http://localhost:8080')
    except Exception as e:
        print(f'打开浏览器失败: {e}')

if __name__ == '__main__':
    # 启动Vue开发服务器
    start_vue_server()
    # 自动打开浏览器
    open_browser()
    # 启动Flask服务器
    app.run(debug=True, port=5000)
