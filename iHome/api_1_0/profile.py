# -*- coding:utf-8 -*-

from . import api
from flask import session,current_app,jsonify,request
from iHome.models import User
from iHome.utils.image_storage import upload_image
from iHome.utils.response_code import RET
from iHome import constants,db

@api.route('/users/avatar',methods=['POST'])
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

    user_id = session.get('user_id')
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
def get_user_auth():
    user_id = session.get('user_id')
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询用户数据失败')
    if not user:
        return jsonify(errno=RET.NODATA, errmsg='用户不存在')
    response_data = user.to_dict()
    return jsonify(errno=RET.OK, errmsg='OK', data=response_data)