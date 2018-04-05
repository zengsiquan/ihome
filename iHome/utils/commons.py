# -*- coding:utf-8 -*-

from werkzeug.routing import BaseConverter
from flask import session,jsonify
from iHome.utils.response_code import RET
from functools import wraps

class RegexConverter(BaseConverter):
        """自定义正则转换器"""
        def __init__(self,url_map,*args):
            super(RegexConverter,self).__init__(url_map)
            self.regex = args[0]

def login_required(view_func):
    "检验用户是否是登录用户"
    # 装饰器装饰一个函数时，会修改该函数的__name__属性
    # 如果希望装饰器装饰之后的函数，依然保留原始的名字和说明文档,就需要使用wraps装饰器，装饰内存函数
    @wraps(view_func)
    def wrapper(*args,**kwargs):
        user_id = session.get('user_id')
        if not user_id:
            return jsonify(errno=RET.SESSIONERR,errmsg='用户未登录')
        else:
            return view_func(*args,**kwargs)
    return wrapper
