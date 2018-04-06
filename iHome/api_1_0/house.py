# -*- coding:utf-8 -*-

from . import api
from flask import current_app,jsonify
from iHome.models import Area
from iHome.utils.response_code import RET

@api.route('/areas')
def get_areas():
    """提供城区信息
    1.查询所有的城区信息
    2.构造响应数据
    3.响应结果
    """
    try:
        areas = Area.query.all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询城区信息失败')
    # 2.构造响应数据
    area_dict_list = []
    for area in areas:
        area_dict_list.append(area.to_dict())

    return jsonify(errno=RET.OK, errmsg='OK', data=area_dict_list)
