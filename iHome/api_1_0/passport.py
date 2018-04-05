# -*- coding:utf-8 -*-

from . import api
from iHome import redis_store,db
from flask import request,jsonify,current_app,session
from iHome.utils.response_code import RET
from iHome.models import User
from iHome.utils.commons import login_required
import logging
import re

@api.route('/users', methods=['POST'])
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
    json_dict = request.json
    # json_str = request.data
    # json_dict = json.loads(json_str)

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

    if User.query.filter(User.mobile == mobile).first():
        return jsonify(errno=RET.DATAEXIST, errmsg='该⼿手机号已注册')
    # 5.创建用户类的模型类对象（存储于数据库中）
    user = User()
    user.name = mobile
    user.mobile = mobile
    user.password = password
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR,errmsg='保存注册数据失败')
    # 注册成功后保存用户状态保持信息到session
    session['user_id'] = user.id
    session['name'] = user.name
    session['mobile'] = user.mobile
    # 6.给前端响应数据
    return jsonify(errno=RET.OK,errmsg='保存注册数据成功')

@api.route('/sessions',methods=['POST'])
def login():
    json_dict = request.json
    mobile = json_dict.get('mobile')
    password = json_dict.get('password')

    if not all([mobile,password]):
        return jsonify(errno=RET.PARAMERR,errmsg='缺少参数')
    if not re.match(r'^1[345678][0-9]{9}$',mobile):
        return jsonify(errno=RET.PARAMERR, errmsg='手机号码错误')
    try:
        user = User.query.filter(User.mobile == mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg='查询⽤用户失败')
    if not user:
        return jsonify(errno=RET.USERERR,errmsg='⽤用户名或密码错误')
    # 密码校验
    if not user.check_password(password):
        return jsonify(errno=RET.PWDERR, errmsg='用户名或密码错误')

    #状态信息保存在session中
    session['user_id'] = user.id
    session['name'] = user.name
    session['mobile'] = user.mobile

    return jsonify(errno=RET.OK,errmsg='登录成功')

@api.route('/sessions',methods=['DELETE'])
@login_required
def logout():
    session.pop('user_id')
    session.pop('mobile')
    session.pop('name')
    return jsonify(errno=RET.OK,errmsg='退出登录成功')

