import json
import os
import uuid
import datetime

tasks = {}
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.json')

home_data = {}
HOME_DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'home_data.json')

ai_settings = {}
AI_DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ai_data.json')

reply_history = {}
REPLY_HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reply_history.json')

def load_tasks():
    global tasks
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                tasks = json.load(f)
        else:
            tasks = {}
    except json.JSONDecodeError as e:
        tasks = {}
    except Exception as e:
        tasks = {}
    return tasks

def load_home_data():
    global home_data
    try:
        if os.path.exists(HOME_DATA_FILE):
            with open(HOME_DATA_FILE, 'r', encoding='utf-8') as f:
                home_data = json.load(f)
        else:
            home_data = {
                "pricingPlans": [],
                "keyMetrics": [],
                "dashboardData": [],
                "testimonials": []
            }
    except json.JSONDecodeError as e:
        home_data = {
            "pricingPlans": [],
            "keyMetrics": [],
            "dashboardData": [],
            "testimonials": []
        }
    except Exception as e:
        home_data = {
            "pricingPlans": [],
            "keyMetrics": [],
            "dashboardData": [],
            "testimonials": []
        }
    return home_data


def get_ai_stats():
    global reply_history

    stats = {
        'replyRate': 0,
        'averageTime': 0,
        'satisfactionRate': 100,
    }
    
    if not reply_history:
        return stats
    
    total_messages = len(reply_history)
    replied_messages = sum(1 for item in reply_history if item.get('status') == 'replied')
    stats['replyRate'] = round((replied_messages / total_messages) * 100, 2) if total_messages > 0 else 0
    
    response_times = []
    for item in reply_history:
        if item.get('status') == 'replied' and 'responseTime' in item:
            response_times.append(item['responseTime'])
    
    stats['averageTime'] = round(sum(response_times) / len(response_times), 2) if response_times else 0    
    return stats


def save_tasks():
    try:
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
    except Exception as e:
        import traceback
        traceback.print_exc()


def load_ai_data():
    global ai_settings, reply_history
    try:
        if os.path.exists(AI_DATA_FILE):
            with open(AI_DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                ai_settings = data.get('settings', {})
                reply_history = data.get('history', [])
    except Exception as e:
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
    required_fields = ['aiStatus', 'replyDelay', 'minReplyInterval', 'contactPerson', 'aiPersona', 'customRules']
    for field in required_fields:
        if field not in settings_data:
            print(f'警告: 设置数据中缺少字段 {field}')
            if field == 'aiStatus':
                settings_data[field] = False
            elif field == 'replyDelay':
                settings_data[field] = 5
            elif field == 'minReplyInterval':
                settings_data[field] = 60
            elif field == 'contactPerson':
                settings_data[field] = ''
            elif field == 'aiPersona':
                settings_data[field] = '我是一个友好、专业的AI助手，致力于为用户提供准确、及时的帮助。'
            elif field == 'customRules':
                settings_data[field] = []

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

load_tasks()
load_ai_data()
load_home_data()