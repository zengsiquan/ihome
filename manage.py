# -*- coding:utf-8 -*-

#导入Flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf.csrf import CsrfProtect



class Config(object):
    DEBUG = True
    #配置数据库
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/iHome'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 配置redis
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    SECTRY_KEY = '6ZgzrGKm4oG+W5E0cVzG5q5zp/iUHUckGwpyQVMrnpWxCPa0Yw59n9Wf+UN0n1ET'


app = Flask(__name__)
CsrfProtect(app)

#注册数据库
app.config.from_object(Config)
db = SQLAlchemy(app)
redis_store = redis.StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT)

#定义视图函数
@app.route('/')
def index():
    return 'index'

#启动该应用的入口
if __name__ == '__main__':
    # 启动应用
    app.run()