# -*- coding:utf-8 -*-
from werkzeug.routing import BaseConverter


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import redis
from flask_session import Session
from config import configs
from utils.commons import RegexConverter
import logging


db = SQLAlchemy()
redis_store = None

# 设置日志的记录等级
logging.basicConfig(level=logging.DEBUG)  # 调试debug级
# 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
file_log_handler = logging.FileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
# 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象（flask app使用的）添加日志记录器
logging.getLogger().addHandler(file_log_handler)
def get_app(config_name):
    app = Flask(__name__)

    app.config.from_object(configs[config_name])
    # app.config['secret_key'] = '6ZgzrGKm4oG+W5E0cVzG5q5zp/iUHUckGwpyQVMrnpWxCPa0Yw59n9Wf+UN0n1ET'
    # app.secret_key = 'l40oG7xuqCMyNBDE+qfibfk1CYCitMZ7fibPFQBduCZKn22sTzDSP1mUchEMDBPq'
    db.init_app(app)

    global redis_store
    redis_store = redis.StrictRedis(host=configs[config_name].REDIS_HOST,port=configs[config_name].REDIS_PORT)

    # SESSION_TYPE = 'redis'
    # SESSION_REDIS = redis.StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT)
    # SESSION_USE_SIGNER = True
    # PERMANENT_SESSION_LIFETIME = 3600 * 24

    # manager = Manager(app)
    # Migrate(app,db)
    # manager.add_command('db',MigrateCommand)

    CSRFProtect(app)
    Session(app)

    app.url_map.converters['re'] = RegexConverter

    import api_1_0
    app.register_blueprint(api_1_0.api)

    import web_html
    app.register_blueprint(web_html.html)


    return app