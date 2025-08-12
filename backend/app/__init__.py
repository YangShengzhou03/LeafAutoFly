import os
from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from app.config import config_by_name
from app.utils.helpers import ensure_data_directories

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    
    # 初始化扩展
    CORS(app)
    login_manager.init_app(app)
    
    # 确保数据目录存在
    ensure_data_directories()
    
    # 注册蓝图
    from app.routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from app.routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    from app.routes.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    # 注册错误处理器
    from app.errors.handlers import register_error_handlers
    register_error_handlers(app)
    
    return app
