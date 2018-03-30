# -*- coding:utf-8 -*-

#导入Flask
from flask import Flask


class Config(object):
    DEBUG = True

    #配置数据库
    # 配置redis

app = Flask(__name__)

#注册数据库
app.config.from_object(Config)
#定义视图函数
@app.route('/')
def index():
    return

#启动该应用的入口
if __name__ == '__main__':
    # 启动应用
    app.run()