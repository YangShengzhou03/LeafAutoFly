import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-for-development-only')
    JSON_SORT_KEYS = False
    DATA_DIRECTORY = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    USERS_JSON_PATH = os.path.join(DATA_DIRECTORY, 'users.json')
    EXAMPLES_JSON_PATH = os.path.join(DATA_DIRECTORY, 'examples.json')
    JWT_EXPIRATION_DELTA = timedelta(days=1)

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    DATA_DIRECTORY = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests', 'test_data')

class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')  # 生产环境必须设置环境变量

config_by_name = {
    'dev': DevelopmentConfig,
    'test': TestingConfig,
    'prod': ProductionConfig,
    'default': DevelopmentConfig
}
