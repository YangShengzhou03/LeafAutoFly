import json
import os
import uuid
import datetime

tasks = {}
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.json')

ai_settings = {}
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
    return tasks


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
    return ai_settings, reply_history


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


def add_task(task_data):
    task_id = str(uuid.uuid4())
    task_data['id'] = task_id
    task_data['createdAt'] = datetime.datetime.now().isoformat()
    tasks[task_id] = task_data
    save_tasks()
    return task_data


def delete_task(task_id):
    if task_id in tasks:
        del tasks[task_id]
        save_tasks()
        return True
    return False


def update_task_status(task_id, status):
    if task_id not in tasks:
        return None
    
    tasks[task_id]['status'] = status
    tasks[task_id]['updatedAt'] = datetime.datetime.now().isoformat()
    save_tasks()
    
    return tasks[task_id]


def clear_tasks():
    tasks.clear()
    save_tasks()
    return True


def save_ai_settings(settings_data):
    global ai_settings
    ai_settings = settings_data
    ai_settings['updatedAt'] = datetime.datetime.now().isoformat()
    save_ai_data()
    return ai_settings


def add_ai_history(history_data):
    global reply_history
    history_data['id'] = str(uuid.uuid4())
    history_data['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    reply_history.append(history_data)
    save_ai_data()
    return history_data

# 初始化数据
load_tasks()
load_ai_data()