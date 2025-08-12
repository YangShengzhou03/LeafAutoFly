from app.config import Config
from app.models.user import User
from app.utils.helpers import read_json_file, write_json_file, generate_id, get_current_timestamp

def get_users():
    """获取所有用户"""
    users_data = read_json_file(Config.USERS_JSON_PATH)
    return [User.from_dict(data) for data in users_data]

def get_user_by_id(user_id):
    """通过ID获取用户"""
    users = get_users()
    for user in users:
        if user.id == user_id:
            return user
    return None

def get_user_by_username(username):
    """通过用户名获取用户"""
    users = get_users()
    for user in users:
        if user.username == username:
            return user
    return None

def get_user_by_email(email):
    """通过邮箱获取用户"""
    users = get_users()
    for user in users:
        if user.email == email:
            return user
    return None

def create_user(username, email, password):
    """创建新用户"""
    # 检查用户名和邮箱是否已存在
    if get_user_by_username(username):
        raise ValueError("用户名已存在")
    if get_user_by_email(email):
        raise ValueError("邮箱已存在")
    
    # 创建新用户
    user = User(
        id=generate_id(),
        username=username,
        email=email,
        password_hash=""
    )
    user.set_password(password)
    
    # 设置时间戳
    timestamp = get_current_timestamp()
    user.created_at = timestamp
    user.updated_at = timestamp
    
    # 保存到JSON文件
    users = get_users()
    users.append(user)
    write_json_file(Config.USERS_JSON_PATH, [u.to_dict() for u in users])
    
    return user

def update_user(user_id, **kwargs):
    """更新用户信息"""
    users = get_users()
    for i, user in enumerate(users):
        if user.id == user_id:
            # 更新字段
            if 'username' in kwargs:
                user.username = kwargs['username']
            if 'email' in kwargs:
                user.email = kwargs['email']
            if 'password' in kwargs:
                user.set_password(kwargs['password'])
            
            # 更新时间戳
            user.updated_at = get_current_timestamp()
            
            # 保存更改
            users[i] = user
            write_json_file(Config.USERS_JSON_PATH, [u.to_dict() for u in users])
            return user
    
    return None

def delete_user(user_id):
    """删除用户"""
    users = get_users()
    users = [u for u in users if u.id != user_id]
    write_json_file(Config.USERS_JSON_PATH, [u.to_dict() for u in users])
    return True
