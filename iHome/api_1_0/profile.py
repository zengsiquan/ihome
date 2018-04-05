# -*- coding:utf-8 -*-

from . import api
from flask import session,current_app,jsonify
from iHome.models import User
from iHome.utils.response_code import RET

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