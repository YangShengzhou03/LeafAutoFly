from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
    def __init__(self, id, username, email, password_hash, created_at=None, updated_at=None):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at
        self.updated_at = updated_at

    def set_password(self, password):
        """设置密码哈希"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """转换为字典用于JSON序列化"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @classmethod
    def from_dict(cls, data):
        """从字典创建User实例"""
        return cls(
            id=data.get('id'),
            username=data.get('username'),
            email=data.get('email'),
            password_hash=data.get('password_hash'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
