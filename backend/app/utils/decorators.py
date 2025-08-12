from functools import wraps
from flask import jsonify, request
from flask_login import current_user

def token_required(f):
    """验证令牌的装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # 从请求头获取令牌
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'message': '令牌缺失!'}), 401
        
        # 这里应该验证令牌的有效性
        # 简化处理，实际应用中应该使用JWT等机制验证
        if token != 'dummy-token-for-development':
            return jsonify({'message': '令牌无效!'}), 401
        
        return f(*args, **kwargs)
    return decorated

def login_required(f):
    """验证用户是否已登录的装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'message': '请先登录!'}), 401
        return f(*args, **kwargs)
    return decorated
