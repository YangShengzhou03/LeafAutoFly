import random
import uuid
from datetime import datetime, timedelta

import pytz
from flask import Flask, render_template, jsonify, request
from flask_apscheduler import APScheduler

# 初始化Flask应用
app = Flask(__name__)
app.config.from_object('config')

# 初始化调度器
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

# 内存数据库 - 存储任务
tasks_db = []

# 内存数据库 - 存储AI对话历史
ai_conversations = []

# 任务执行日志
task_execution_logs = []

# 系统设置
system_settings = {
    "theme": "auto",
    "themeColor": "#409eff",
    "notifications": True,
    "timezone": "Asia/Shanghai"
}

# 辅助函数 - 获取时区
def get_timezone():
    return pytz.timezone(system_settings["timezone"])

# 辅助函数 - 获取当前时间
def get_current_time():
    return datetime.now(get_timezone()).isoformat()

# 任务执行函数
def execute_task(task_id):
    """执行任务的函数"""
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    if task:
        # 更新任务状态
        task["status"] = "running"
        
        # 记录任务执行日志
        execution_time = get_current_time()
        task_execution_logs.append({
            "id": str(uuid.uuid4()),
            "task_id": task_id,
            "task_name": task["name"],
            "start_time": execution_time,
            "status": "completed"
        })
        
        print(f"任务 '{task['name']}' 执行中...")

# 路由 - 首页
@app.route('/')
def index():
    return render_template('index.html')

# 路由 - 任务调度页面
@app.route('/scheduler')
def scheduler_page():
    return render_template('pages/scheduler.html')

# 路由 - AI助手页面
@app.route('/ai')
def ai_page():
    return render_template('pages/ai.html')

# 路由 - 设置页面
@app.route('/settings')
def settings_page():
    return render_template('pages/settings.html')

# API - 获取所有任务
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks_db)

# API - 获取任务执行日志
@app.route('/api/tasks/logs', methods=['GET'])
def get_task_logs():
    return jsonify(task_execution_logs)

# API - 创建新任务
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
    
    # 添加到数据库
    tasks_db.append(new_task)
    
    # 根据任务类型添加到调度器
    if new_task["type"] == "once":
        # 一次性任务
        exec_time = datetime.fromisoformat(new_task["executionTime"])
        scheduler.add_job(
            id=task_id,
            func=execute_task,
            args=[task_id],
            run_date=exec_time,
            timezone=get_timezone()
        )
    elif new_task["type"] == "scheduled":
        # 定时任务 (Cron)
        scheduler.add_job(
            id=task_id,
            func=execute_task,
            args=[task_id],
            trigger='cron',
            expression=new_task["cronExpression"],
            timezone=get_timezone()
        )
    elif new_task["type"] == "interval":
        # 间隔任务
        interval_args = {new_task["intervalUnit"]: new_task["intervalValue"]}
        scheduler.add_job(
            id=task_id,
            func=execute_task,
            args=[task_id],
            trigger='interval',
            **interval_args,
            timezone=get_timezone()
        )
    
    return jsonify(new_task), 201

# API - 更新任务
@app.route('/api/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    if not task:
        return jsonify({"error": "任务不存在"}), 404
    
    data = request.get_json()
    
    # 更新任务信息
    task["name"] = data.get("name", task["name"])
    task["description"] = data.get("description", task["description"])
    task["updatedAt"] = get_current_time()
    
    # 如果任务类型或时间参数改变，重新调度
    type_changed = data.get("type") and data.get("type") != task["type"]
    time_changed = False
    
    if data.get("type") == "once" and data.get("executionTime") != task["executionTime"]:
        time_changed = True
    elif data.get("type") == "scheduled" and data.get("cronExpression") != task["cronExpression"]:
        time_changed = True
    elif data.get("type") == "interval":
        if (data.get("intervalValue") != task["intervalValue"] or 
            data.get("intervalUnit") != task["intervalUnit"]):
            time_changed = True
    
    # 如果类型或时间改变，重新设置任务
    if type_changed or time_changed:
        # 先移除旧任务
        if scheduler.get_job(task_id):
            scheduler.remove_job(task_id)
        
        # 更新任务类型和时间参数
        task["type"] = data.get("type", task["type"])
        task["executionTime"] = data.get("executionTime", task["executionTime"])
        task["cronExpression"] = data.get("cronExpression", task["cronExpression"])
        task["intervalValue"] = data.get("intervalValue", task["intervalValue"])
        task["intervalUnit"] = data.get("intervalUnit", task["intervalUnit"])
        
        # 添加新任务调度
        if task["type"] == "once":
            exec_time = datetime.fromisoformat(task["executionTime"])
            scheduler.add_job(
                id=task_id,
                func=execute_task,
                args=[task_id],
                run_date=exec_time,
                timezone=get_timezone()
            )
        elif task["type"] == "scheduled":
            scheduler.add_job(
                id=task_id,
                func=execute_task,
                args=[task_id],
                trigger='cron',
                expression=task["cronExpression"],
                timezone=get_timezone()
            )
        elif task["type"] == "interval":
            interval_args = {task["intervalUnit"]: task["intervalValue"]}
            scheduler.add_job(
                id=task_id,
                func=execute_task,
                args=[task_id],
                trigger='interval',** interval_args,
                timezone=get_timezone()
            )
    
    return jsonify(task)

# API - 删除任务
@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks_db
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    if not task:
        return jsonify({"error": "任务不存在"}), 404
    
    # 从调度器中移除任务
    if scheduler.get_job(task_id):
        scheduler.remove_job(task_id)
    
    # 从数据库中删除任务
    tasks_db = [t for t in tasks_db if t["id"] != task_id]
    
    return jsonify({"message": "任务已删除"})

# API - 开始任务
@app.route('/api/tasks/<task_id>/start', methods=['POST'])
def start_task(task_id):
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    if not task:
        return jsonify({"error": "任务不存在"}), 404
    
    # 更新任务状态
    task["status"] = "running"
    task["updatedAt"] = get_current_time()
    
    # 如果任务已暂停，重新添加到调度器
    if not scheduler.get_job(task_id):
        if task["type"] == "once":
            exec_time = datetime.fromisoformat(task["executionTime"])
            scheduler.add_job(
                id=task_id,
                func=execute_task,
                args=[task_id],
                run_date=exec_time,
                timezone=get_timezone()
            )
        elif task["type"] == "scheduled":
            scheduler.add_job(
                id=task_id,
                func=execute_task,
                args=[task_id],
                trigger='cron',
                expression=task["cronExpression"],
                timezone=get_timezone()
            )
        elif task["type"] == "interval":
            interval_args = {task["intervalUnit"]: task["intervalValue"]}
            scheduler.add_job(
                id=task_id,
                func=execute_task,
                args=[task_id],
                trigger='interval',
                **interval_args,
                timezone=get_timezone()
            )
    
    return jsonify({"message": "任务已启动"})

# API - 暂停任务
@app.route('/api/tasks/<task_id>/pause', methods=['POST'])
def pause_task(task_id):
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    if not task:
        return jsonify({"error": "任务不存在"}), 404
    
    # 更新任务状态
    task["status"] = "paused"
    task["updatedAt"] = get_current_time()
    
    # 从调度器中移除但不删除任务
    if scheduler.get_job(task_id):
        scheduler.remove_job(task_id)
    
    return jsonify({"message": "任务已暂停"})

# API - 标记任务为完成
@app.route('/api/tasks/<task_id>/complete', methods=['POST'])
def complete_task(task_id):
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    if not task:
        return jsonify({"error": "任务不存在"}), 404
    
    # 更新任务状态
    task["status"] = "completed"
    task["progress"] = 100
    task["updatedAt"] = get_current_time()
    
    # 对于一次性任务，从调度器中移除
    if task["type"] == "once" and scheduler.get_job(task_id):
        scheduler.remove_job(task_id)
    
    return jsonify({"message": "任务已标记为完成"})

# API - 获取AI对话历史
@app.route('/api/ai/conversations', methods=['GET'])
def get_ai_conversations():
    return jsonify(ai_conversations)

# API - 发送AI消息
@app.route('/api/ai/message', methods=['POST'])
def send_ai_message():
    data = request.get_json()
    user_message = data.get("message", "")
    
    if not user_message:
        return jsonify({"error": "消息不能为空"}), 400
    
    # 生成消息ID和时间
    message_id = str(uuid.uuid4())
    current_time = get_current_time()
    
    # 添加用户消息到对话历史
    user_msg = {
        "id": message_id,
        "sender": "user",
        "content": user_message,
        "timestamp": current_time
    }
    ai_conversations.append(user_msg)
    
    # 生成AI回复 (简单模拟)
    ai_responses = [
        "我理解你的需求，这是一个很好的想法。",
        "根据你的问题，我建议你尝试以下方法...",
        "这个问题有点复杂，让我仔细分析一下。",
        "我已经记录了你的请求，会尽快处理。",
        "关于这个主题，我可以提供更多详细信息。",
        "你的问题很有价值，这是我对它的看法...",
        "我建议你考虑其他可能性，比如..."
    ]
    
    ai_message_id = str(uuid.uuid4())
    ai_msg = {
        "id": ai_message_id,
        "sender": "ai",
        "content": random.choice(ai_responses),
        "timestamp": get_current_time()
    }
    ai_conversations.append(ai_msg)
    
    # 返回AI回复
    return jsonify(ai_msg)

# API - 清除AI对话历史
@app.route('/api/ai/conversations', methods=['DELETE'])
def clear_ai_conversations():
    global ai_conversations
    ai_conversations = []
    return jsonify({"message": "对话历史已清除"})

# API - 获取系统设置
@app.route('/api/settings', methods=['GET'])
def get_settings():
    return jsonify(system_settings)

# API - 更新系统设置
@app.route('/api/settings', methods=['PUT'])
def update_settings():
    data = request.get_json()
    
    # 更新设置
    for key, value in data.items():
        if key in system_settings:
            system_settings[key] = value
    
    return jsonify(system_settings)

# 创建示例任务
def create_sample_tasks():
    """创建示例任务用于演示"""
    if not tasks_db:  # 仅当数据库为空时创建示例任务
        current_time = get_current_time()
        
        # 示例1: 一次性任务
        one_time = datetime.now(get_timezone()) + timedelta(minutes=30)
        tasks_db.append({
            "id": str(uuid.uuid4()),
            "name": "系统备份",
            "description": "备份系统重要数据",
            "type": "once",
            "executionTime": one_time.isoformat(),
            "cronExpression": "",
            "intervalValue": 1,
            "intervalUnit": "hours",
            "status": "pending",
            "progress": 0,
            "createdAt": current_time,
            "updatedAt": current_time
        })
        
        # 示例2: 定时任务
        tasks_db.append({
            "id": str(uuid.uuid4()),
            "name": "日志清理",
            "description": "清理30天前的系统日志",
            "type": "scheduled",
            "executionTime": "",
            "cronExpression": "0 0 * * 0",  # 每周日凌晨执行
            "intervalValue": 1,
            "intervalUnit": "hours",
            "status": "pending",
            "progress": 0,
            "createdAt": current_time,
            "updatedAt": current_time
        })
        
        # 示例3: 间隔任务
        tasks_db.append({
            "id": str(uuid.uuid4()),
            "name": "性能监控",
            "description": "定期检查系统性能",
            "type": "interval",
            "executionTime": "",
            "cronExpression": "",
            "intervalValue": 2,
            "intervalUnit": "hours",  # 每2小时执行一次
            "status": "pending",
            "progress": 0,
            "createdAt": current_time,
            "updatedAt": current_time
        })

# 应用启动时创建示例任务
with app.app_context():
    create_sample_tasks()

# 启动应用
if __name__ == '__main__':
    app.run(debug=True)
