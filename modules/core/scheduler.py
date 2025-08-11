from datetime import datetime
from extensions import db
from models import Task

class TaskScheduler:
    """任务调度核心逻辑"""
    
    @staticmethod
    def get_task_status(task_id):
        """获取任务状态"""
        task = Task.query.get(task_id)
        if not task:
            return None
        
        return {
            "id": task.id,
            "name": task.name,
            "status": task.status,
            "last_run": task.last_run.isoformat() if task.last_run else None,
            "next_run": task.next_run.isoformat() if task.next_run else None
        }
    
    @staticmethod
    def update_task_status(task_id, status):
        """更新任务状态"""
        task = Task.query.get(task_id)
        if not task:
            return False
        
        task.status = status
        db.session.commit()
        return True
    
    @staticmethod
    def get_recent_tasks(limit=10):
        """获取最近的任务"""
        return Task.query.order_by(Task.created_at.desc()).limit(limit).all()
    
    @staticmethod
    def get_task_execution_stats():
        """获取任务执行统计信息"""
        total = Task.query.count()
        active = Task.query.filter_by(status='active').count()
        paused = Task.query.filter_by(status='paused').count()
        
        # 有执行记录的任务
        executed = Task.query.filter(Task.last_run.isnot(None)).count()
        
        return {
            "total": total,
            "active": active,
            "paused": paused,
            "executed": executed
        }
