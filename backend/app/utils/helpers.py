import os
import json
import uuid
from datetime import datetime
from app import login_manager
from app.models.user import User

def ensure_data_directories():
    """确保数据目录存在"""
    from app.config import Config
    if not os.path.exists(Config.DATA_DIRECTORY):
        os.makedirs(Config.DATA_DIRECTORY)
    
    # 确保基础JSON文件存在
    ensure_json_file(Config.USERS_JSON_PATH, [])
    ensure_json_file(Config.EXAMPLES_JSON_PATH, [])

def ensure_json_file(file_path, default_content):
    """确保JSON文件存在，不存在则创建并写入默认内容"""
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(default_content, f, ensure_ascii=False, indent=2)

def read_json_file(file_path):
    """读取JSON文件内容"""
    ensure_json_file(file_path, [])
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def write_json_file(file_path, data):
    """写入数据到JSON文件"""
    ensure_json_file(file_path, [])
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def generate_id():
    """生成唯一ID"""
    return str(uuid.uuid4())

def get_current_timestamp():
    """获取当前时间戳"""
    return datetime.utcnow().isoformat()

@login_manager.user_loader
def load_user(user_id):
    """加载用户用于Flask-Login"""
    from app.services.auth_service import get_user_by_id
    return get_user_by_id(user_id)
