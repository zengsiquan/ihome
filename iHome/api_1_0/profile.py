# -*- coding:utf-8 -*-

from . import api
from flask import session,g,current_app,jsonify,request
from iHome.models import User
from iHome.utils.image_storage import upload_image
from iHome.utils.response_code import RET
from iHome import constants,db
from iHome.utils.commons import login_required

@api.route('/users/avatar',methods=['POST'])
@login_required
def upload_avatar():
    """提供用户头像上传
    0. TODO 先判断用户是否登录
    1. 获取图片数据
    2. 调用上传工具进行图片上传
    3. 获取返回的值，存储到数据库中并拼接出图片路由
    4. 响应上传结果
    """
    try:
        image_data = request.files.get('avatar')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='头像参数错误')
    try:
        key = upload_image(image_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg='上传头像失败')

    # user_id = session.get('user_id')
    user_id = g.user_id
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询用户数据失败')

    if not user:
        return jsonify(errno=RET.NODATA, errmsg='用户不存在')

    user.avatar_url = key

    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='存储用户头像地址失败')

    avatar_url = constants.QINIU_DOMIN_PREFIX + key
    print (avatar_url)
    return jsonify(errno=RET.OK,errmsg='上传头像成功',data=avatar_url)

@api.route('/users')
@login_required
def get_user_auth():
    # user_id = session.get('user_id')
    user_id = g.user_id
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询用户数据失败')
    if not user:
        return jsonify(errno=RET.NODATA, errmsg='用户不存在')
    response_data = user.to_dict()
    return jsonify(errno=RET.OK, errmsg='OK', data=response_data)

@api.route('/users/name',methods=['PUT'])
@login_required
def set_user_name():
    # 0. TODO  先判断用户是否登录
    # 1.接受用户传入的新名字， new_name
    json_dict = request.json
    new_name = json_dict.get('name')

    # 2.判断参数是否为空
    if not new_name:
        return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')

    # 3.查询当前登录用户
    # user_id = session.get('user_id')
    user_id = g.user_id
    try:
        user = user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询用户数据失败')
    if not user:
        return jsonify(errno=RET.NODATA, errmsg='用户不存在')

    # 4.将new_name赋值给当前的登录用户的name属性
    user.name = new_name

    # 5.将新的数据写入到数据库
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='存储用户名失败')

    # 6.响应结果
    return jsonify(errno=RET.OK, errmsg='修改用户名成功')