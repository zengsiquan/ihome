# -*- coding:utf-8 -*-
from werkzeug.routing import BaseConverter


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from config import Config,DevelopmentConfig
from flask_wtf.csrf import CSRFProtect
import redis
from flask_session import Session
from config import configs


db = SQLAlchemy()
redis_store = None
def get_app(config_name):
    app = Flask(__name__)
    app.config.from_object(configs[config_name])
    # app.config['secret_key'] = '6ZgzrGKm4oG+W5E0cVzG5q5zp/iUHUckGwpyQVMrnpWxCPa0Yw59n9Wf+UN0n1ET'
    # app.secret_key = 'l40oG7xuqCMyNBDE+qfibfk1CYCitMZ7fibPFQBduCZKn22sTzDSP1mUchEMDBPq'


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
    return app