# -*- coding:utf-8 -*-

from . import api
from iHome import redis_store,db
from flask import request,jsonify
from iHome.utils.response_code import RET
from iHome.models import User
import logging

@api.route('/users',method=['POST'])
def register():
    """实现注册
       1.获取请求参数：手机号，短信验证码，密码
       2.判断参数是否缺少
       3.获取服务器的短信验证码
       4.并与客户端传入的验证码比较,如果一致
       5.创建User模型类对象
       6.保存注册数据到数据库
       7.响应结果
    """

    # 1.获取请求参数：手机号，短信验证码，密码
    # json_dict = request.json
    json_str = request.data
    json_dict = json_str.loads(json_str)

    mobile = json_dict.get('mobile')
    mes_code = json_dict.get('mes_code')
    password = json_dict.get('password')

    # 2.判断参数是否缺少
    if not all([mobile, mes_code, password]):
        return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')
    # 3.匹配手机号

    # 4.对短信验证码进行验证
    try:
        redis_code = redis_store.get('Mobile:' + mobile)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询短信验证码失败')
    if not redis_code:
        return jsonify(errno=RET.NODATA, errmsg='短信验证码不存在')

    if mes_code != redis_code:
        return jsonify(errno=RET.DATAERR, errmsg='输入验证码有误')

    # 5.创建用户类的模型类对象（存储于数据库中）
    user = User()
    user.name = mobile
    user.mobile = mobile
    user.password_hash = password
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        return jsonify(RET.DBERR,errmsg='保存注册数据失败')

    # 6.给前端响应数据
    return jsonify(RET.OK,errmsg='保存注册数据失败')
