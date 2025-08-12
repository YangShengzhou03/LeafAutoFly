from flask import Blueprint, jsonify, render_template
from flask_login import current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """根路径路由，返回API信息"""
    return jsonify({
        'message': '欢迎使用LeafAuto Web API',
        'endpoints': {
            'auth': {
                'login': '/auth/login',
                'register': '/auth/register',
                'logout': '/auth/logout',
                'profile': '/auth/profile'
            },
            'examples': {
                'list': '/api/examples',
                'create': '/api/examples',
                'get': '/api/examples/<id>',
                'update': '/api/examples/<id>',
                'delete': '/api/examples/<id>'
            }
        }
    })

@main.route('/health')
def health_check():
    """健康检查路由"""
    return jsonify({'status': 'healthy', 'service': 'leafauto-api'})
