from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.services.auth_service import (
    get_user_by_username, get_user_by_id, create_user, update_user
)

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': '请提供用户名和密码'}), 400
    
    user = get_user_by_username(data['username'])
    
    if not user or not user.check_password(data['password']):
        return jsonify({'message': '用户名或密码错误'}), 401
    
    # 登录用户
    login_user(user)
    
    return jsonify({
        'message': '登录成功',
        'user': user.to_dict()
    })

@auth.route('/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'message': '请提供完整的用户信息'}), 400
    
    try:
        user = create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        return jsonify({
            'message': '注册成功',
            'user': user.to_dict()
        }), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400

@auth.route('/logout')
@login_required
def logout():
    """用户登出"""
    logout_user()
    return jsonify({'message': '成功登出'})

@auth.route('/profile')
@login_required
def profile():
    """获取当前用户信息"""
    return jsonify({'user': current_user.to_dict()})

@auth.route('/profile', methods=['PUT'])
@login_required
def update_profile():
    """更新当前用户信息"""
    data = request.get_json()
    
    if not data:
        return jsonify({'message': '请提供更新的信息'}), 400
    
    user = update_user(current_user.id,** data)
    
    if not user:
        return jsonify({'message': '更新失败'}), 400
    
    return jsonify({
        'message': '更新成功',
        'user': user.to_dict()
    })

@auth.route('/change-password', methods=['POST'])
@login_required
def change_password():
    """修改密码"""
    data = request.get_json()
    
    if not data or not data.get('old_password') or not data.get('new_password'):
        return jsonify({'message': '请提供旧密码和新密码'}), 400
    
    # 验证旧密码
    if not current_user.check_password(data['old_password']):
        return jsonify({'message': '旧密码不正确'}), 401
    
    # 更新密码
    user = update_user(current_user.id, password=data['new_password'])
    
    return jsonify({'message': '密码更新成功'})
