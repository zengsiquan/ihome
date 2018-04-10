# -*- coding:utf-8 -*-
#处理订单逻辑
from flask import request,current_app,jsonify,g
from iHome.models import House,Order
from iHome.utils.response_code import RET
from iHome import db
from iHome.utils.commons import login_required
import datetime
from . import api

@api.route('/orders',methods=['POST'])
@login_required
def create_order():
    # 创建，提交订单
    #：house_id, ⼊入住时间和离开时间
    json_dict = request.json
    house_id = json_dict.get('house_id')
    start_date_str = json_dict.get('start_date')
    end_date_str = json_dict.get('end_date')
    # 判断参数是否缺少
    if not all([house_id,start_date_str,end_date_str]):
        return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')
    # 校验房屋是否存在
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询房屋数据失败')
    if not house:
        return jsonify(errno=RET.NODATA, errmsg='房屋不不存在')
    # 对⼊入住和离开时间进⾏行行校验
    try:
        start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')
        if start_date and end_date:
            # 断言：入住时间一定小于离开时间，如果不满足，就抛出异常
            assert start_date < end_date, Exception('入住时间有误')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='⼊入住时间有误')

    try:
        conflict_orders = Order.query.filter(Order.house_id == house_id, end_date > Order.begin_date,
                                         start_date < Order.end_date).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询冲突订单失败')
    if conflict_orders:
        return jsonify(errno=RET.DATAERR, errmsg='该房屋已被预订')

    order = Order()
    order.user_id = g.user_id
    order.house_id = house_id
    order.begin_date = start_date
    order.end_date = end_date
    order.days = (end_date - start_date).days
    order.house_price = house.price
    order.amount = house.price * order.days

    try:
        db.session.add(order)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DATAERR, errmsg='保存订单数据到数据库失败')
    # 6.响应结果
    return jsonify(errno=RET.OK, errmsg='OK')

