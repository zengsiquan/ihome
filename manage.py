# -*- coding:utf-8 -*-

from iHome import db
from iHome import get_app

from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand

# class Config(object):
#     DEBUG = True
#     SECRET_KEY = 'l40oG7xuqCMyNBDE+qfibfk1CYCitMZ7fibPFQBduCZKn22sTzDSP1mUchEMDBPq'
#
#
#     #配置数据库
#     SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/iHome'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     # 配置redis
#     REDIS_HOST = '127.0.0.1'
#     REDIS_PORT = 6379

# app = Flask(__name__)

#注册数据库
# app.config.from_object(Config)
# app.config['secret_key'] = '6ZgzrGKm4oG+W5E0cVzG5q5zp/iUHUckGwpyQVMrnpWxCPa0Yw59n9Wf+UN0n1ET'
# app.secret_key = 'l40oG7xuqCMyNBDE+qfibfk1CYCitMZ7fibPFQBduCZKn22sTzDSP1mUchEMDBPq'

# db = SQLAlchemy(app)

# redis_store = redis.StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT)

# SESSION_TYPE = 'redis'
# SESSION_REDIS = redis.StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT)
# SESSION_USE_SIGNER = True
# PERMANENT_SESSION_LIFETIME = 3600 * 24

app = get_app('development')

manager = Manager(app)
Migrate(app,db)
manager.add_command('db',MigrateCommand)

# CSRFProtect(app)
# Session(app)
#定义视图函数
# @app.route('/')
# def index():
#
#     return 'index'

#启动该应用的入口
if __name__ == '__main__':
    # 启动应用
    manager.run()