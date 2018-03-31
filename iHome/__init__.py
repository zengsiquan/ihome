# -*- coding:utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_wtf.csrf import CSRFProtect
import redis
from flask_session import Session

app = Flask(__name__)
app.config.from_object(Config)
# app.config['secret_key'] = '6ZgzrGKm4oG+W5E0cVzG5q5zp/iUHUckGwpyQVMrnpWxCPa0Yw59n9Wf+UN0n1ET'
# app.secret_key = 'l40oG7xuqCMyNBDE+qfibfk1CYCitMZ7fibPFQBduCZKn22sTzDSP1mUchEMDBPq'

db = SQLAlchemy(app)

redis_store = redis.StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT)

# SESSION_TYPE = 'redis'
# SESSION_REDIS = redis.StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT)
# SESSION_USE_SIGNER = True
# PERMANENT_SESSION_LIFETIME = 3600 * 24

# manager = Manager(app)
# Migrate(app,db)
# manager.add_command('db',MigrateCommand)

CSRFProtect(app)
Session(app)