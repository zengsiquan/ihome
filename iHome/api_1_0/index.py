# -*- coding:utf-8 -*-

from . import api



#定义视图函数
@api.route('/')
def index():

    return 'index'