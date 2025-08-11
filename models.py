from datetime import datetime
from extensions import db

class Task(db.Model):
    """任务模型"""
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    cron_expression = db.Column(db.String(50), nullable=False)  # cron表达式
    status = db.Column(db.String(20), default='active')  # active, paused
    created_at = db.Column(db.DateTime, default=datetime.now)
    last_run = db.Column(db.DateTime, nullable=True)
    next_run = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<Task {self.name}>'

class AIChatMessage(db.Model):
    """AI聊天消息模型"""
    id = db.Column(db.String(36), primary_key=True)
    content = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(20), nullable=False)  # user, assistant
    timestamp = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<Message {self.role}: {self.content[:20]}>'
