import random
import uuid
from datetime import datetime
import pytz
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_cors import CORS

# 初始化Flask应用
app = Flask(__name__)
app.secret_key = 'leafauto_secret_key'  # 用于会话管理
app.config['TEMPLATES_AUTO_RELOAD'] = True

# 启用CORS
CORS(app)

# 内存数据存储 - 替代数据库
tasks_db = []
ai_conversations = []
task_execution_logs = []

# 系统设置
system_settings = {
    "theme": "light",
    "themeColor": "#409eff",
    "notifications": True,
    "timezone": "Asia/Shanghai",
    "systemName": "LeafAuto-Web"
}

# 辅助函数 - 获取时区
def get_timezone():
    return pytz.timezone(system_settings["timezone"])

# 辅助函数 - 获取当前时间
def get_current_time():
    return datetime.now(get_timezone()).isoformat()

# 路由 - 首页
@app.route('/')
def index():
    # 统计数据
    stats = {
        'active_tasks': len([t for t in tasks_db if t['status'] == 'running']),
        'completed_tasks': len([t for t in tasks_db if t['status'] == 'completed']),
        'pending_tasks': len([t for t in tasks_db if t['status'] == 'pending']),
        'ai_interactions': len(ai_conversations)
    }
    return render_template('index.html', stats=stats, settings=system_settings, now=datetime.now())

# 路由 - 任务调度页面
@app.route('/scheduler')
def scheduler_page():
    return render_template('scheduler.html', tasks=tasks_db, settings=system_settings, now=datetime.now())

# 路由 - AI助手页面
@app.route('/ai')
def ai_page():
    return render_template('ai.html', conversations=ai_conversations, settings=system_settings, now=datetime.now())

# 路由 - 设置页面
@app.route('/settings', methods=['GET', 'POST'])
def settings_page():
    if request.method == 'POST':
        # 更新系统设置
        system_settings["theme"] = request.form.get('theme', 'light')
        system_settings["themeColor"] = request.form.get('themeColor', '#409eff')
        system_settings["notifications"] = request.form.get('notifications') == 'on'
        system_settings["timezone"] = request.form.get('timezone', 'Asia/Shanghai')
        system_settings["systemName"] = request.form.get('systemName', 'LeafAuto-Web')
        return redirect(url_for('settings_page'))
    
    return render_template('settings.html', settings=system_settings, now=datetime.now())

# API - 任务管理
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks_db)

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    
    # 生成任务ID
    task_id = str(uuid.uuid4())
    current_time = get_current_time()
    
    # 创建新任务
    new_task = {
        "id": task_id,
        "name": data.get("name", f"任务_{len(tasks_db) + 1}"),
        "description": data.get("description", ""),
        "type": data.get("type", "once"),
        "executionTime": data.get("executionTime"),
        "cronExpression": data.get("cronExpression"),
        "intervalValue": data.get("intervalValue", 1),
        "intervalUnit": data.get("intervalUnit", "hours"),
        "status": "pending",
        "progress": 0,
        "createdAt": current_time,
        "updatedAt": current_time
    }
    
    tasks_db.append(new_task)
    return jsonify(new_task), 201

@app.route('/api/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    task = next((t for t in tasks_db if t['id'] == task_id), None)
    if task:
        return jsonify(task)
    return jsonify({"error": "任务不存在"}), 404

@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks_db
    task = next((t for t in tasks_db if t['id'] == task_id), None)
    if task:
        tasks_db = [t for t in tasks_db if t['id'] != task_id]
        return jsonify({"success": True, "message": "任务删除成功"})
    return jsonify({"success": False, "message": "任务不存在"}), 404

@app.route('/api/tasks/<task_id>/start', methods=['POST'])
def start_task(task_id):
    task = next((t for t in tasks_db if t['id'] == task_id), None)
    if task:
        if task['status'] == 'running':
            return jsonify({"success": False, "message": "任务已在运行中"})
        
        task['status'] = 'running'
        task['updatedAt'] = get_current_time()
        
        # 记录执行日志
        log_entry = {
            "id": str(uuid.uuid4()),
            "taskId": task_id,
            "action": "start",
            "timestamp": get_current_time(),
            "status": "success"
        }
        task_execution_logs.append(log_entry)
        
        return jsonify({"success": True, "message": "任务启动成功"})
    return jsonify({"success": False, "message": "任务不存在"}), 404

@app.route('/api/tasks/<task_id>/complete', methods=['POST'])
def complete_task(task_id):
    task = next((t for t in tasks_db if t['id'] == task_id), None)
    if task:
        task['status'] = 'completed'
        task['progress'] = 100
        task['updatedAt'] = get_current_time()
        
        # 记录执行日志
        log_entry = {
            "id": str(uuid.uuid4()),
            "taskId": task_id,
            "action": "complete",
            "timestamp": get_current_time(),
            "status": "success"
        }
        task_execution_logs.append(log_entry)
        
        return jsonify({"success": True, "message": "任务完成"})
    return jsonify({"success": False, "message": "任务不存在"}), 404

# API - AI聊天
@app.route('/api/ai/chat', methods=['POST'])
def ai_chat():
    data = request.get_json()
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({"error": "消息不能为空"}), 400
    
    # 生成AI回复（模拟）
    ai_response = generate_ai_response(user_message)
    
    # 保存对话记录
    conversation = {
        "id": str(uuid.uuid4()),
        "userMessage": user_message,
        "aiResponse": ai_response,
        "timestamp": get_current_time()
    }
    ai_conversations.append(conversation)
    
    return jsonify({
        "response": ai_response,
        "conversationId": conversation["id"]
    })

def generate_ai_response(user_message):
    """生成AI回复（模拟）"""
    # 简单的关键词匹配回复
    message_lower = user_message.lower()
    
    if any(word in message_lower for word in ['你好', 'hello', 'hi']):
        return "您好！我是您的AI助手，有什么可以帮助您的吗？"
    elif any(word in message_lower for word in ['任务', 'task']):
        return "我可以帮助您管理自动化任务。您可以创建定时任务、设置执行计划，或者查看任务执行状态。"
    elif any(word in message_lower for word in ['帮助', 'help', '怎么']):
        return "我支持以下功能：\n1. 任务管理：创建、编辑、删除自动化任务\n2. 系统监控：查看系统运行状态和统计数据\n3. 智能建议：根据您的需求提供优化建议\n4. 指令执行：执行系统指令和操作"
    elif any(word in message_lower for word in ['状态', 'status', '运行']):
        return "系统当前运行正常，所有服务都在正常运行中。您可以查看仪表盘获取详细的系统状态信息。"
    elif any(word in message_lower for word in ['时间', 'time', '日期']):
        current_time = datetime.now(get_timezone()).strftime('%Y-%m-%d %H:%M:%S')
        return f"当前时间是：{current_time}"
    else:
        return "我理解您的问题，让我为您提供帮助。如果您需要具体的操作指导，请告诉我您想要做什么。"

# API - 主题切换
@app.route('/api/theme', methods=['POST'])
def switch_theme():
    data = request.get_json()
    new_theme = data.get('theme', 'light')
    
    if new_theme in ['light', 'dark']:
        system_settings["theme"] = new_theme
        return jsonify({"success": True, "theme": new_theme})
    
    return jsonify({"success": False, "message": "无效的主题"}), 400

# API - 设置保存
@app.route('/api/settings', methods=['POST'])
def save_settings():
    data = request.get_json()
    
    # 更新系统设置
    if 'theme' in data:
        system_settings["theme"] = data['theme']
    if 'themeColor' in data:
        system_settings["themeColor"] = data['themeColor']
    if 'notifications' in data:
        system_settings["notifications"] = data['notifications']
    if 'timezone' in data:
        system_settings["timezone"] = data['timezone']
    
    return jsonify({"success": True, "message": "设置保存成功"})

# API - 统计数据
@app.route('/api/stats', methods=['GET'])
def get_stats():
    stats = {
        'active_tasks': len([t for t in tasks_db if t['status'] == 'running']),
        'completed_tasks': len([t for t in tasks_db if t['status'] == 'completed']),
        'pending_tasks': len([t for t in tasks_db if t['status'] == 'pending']),
        'failed_tasks': len([t for t in tasks_db if t['status'] == 'failed']),
        'ai_interactions': len(ai_conversations),
        'total_tasks': len(tasks_db),
        'system_uptime': '24小时',
        'last_update': get_current_time()
    }
    return jsonify(stats)

# API - 任务执行日志
@app.route('/api/tasks/<task_id>/logs', methods=['GET'])
def get_task_logs(task_id):
    logs = [log for log in task_execution_logs if log['taskId'] == task_id]
    return jsonify(logs)

# 错误处理
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "页面不存在"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "服务器内部错误"}), 500

# 启动应用
if __name__ == '__main__':
    # 添加一些示例任务
    if not tasks_db:
        sample_tasks = [
            {
                "id": str(uuid.uuid4()),
                "name": "每日数据备份",
                "description": "自动备份系统数据到云端",
                "type": "cron",
                "cronExpression": "0 2 * * *",
                "status": "pending",
                "progress": 0,
                "createdAt": get_current_time(),
                "updatedAt": get_current_time()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "系统健康检查",
                "description": "定期检查系统运行状态",
                "type": "interval",
                "intervalValue": 1,
                "intervalUnit": "hours",
                "status": "running",
                "progress": 45,
                "createdAt": get_current_time(),
                "updatedAt": get_current_time()
            }
        ]
        tasks_db.extend(sample_tasks)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
