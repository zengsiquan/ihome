# -*- coding:utf-8 -*-

from . import api
from iHome.utils.captcha.captcha import captcha
from flask import request,abort,jsonify,make_response,current_app
from iHome import constants
from iHome import redis_store
from iHome.utils.response_code import RET
from iHome.utils.sms import CCP
import logging
import random
import re
import json


@api.route('/image_code')
def get_image_code():
    uuid = request.args.get('uuid')
    print(uuid)
    last_uuid = request.args.get('last_uuid')
    print(last_uuid)
    if not uuid:
        abort(403)
    name,text,image = captcha.generate_captcha()
    logging.debug('图片验证码文字信息：' + text)
    try:
        if last_uuid:

            redis_store.delete('ImageCode:'+last_uuid)


        redis_store.set('ImageCode:'+uuid,text,constants.IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        print e
        logging.error(e)
        # restful要求返回响应状态
        return jsonify(errno=RET.DBERR,errmsg=u'保存验证码失败')
        # 4.返回图片验证码
    resposne = make_response(image)
    resposne.headers['Content-Type'] = 'image/jpg'
    return resposne

@api.route('/mes_code', methods=['POST'])
def send_mes_code():
    # 1. 获取参数:手机号码，图片验证码，uuid
    json_str = request.data
    json_dict = json.loads(json_str)
    mobile = json_dict.get('mobile')
    imagecode = json_dict.get('imagecode')
    uuid = json_dict.get('uuid')

    # 2. 验证参数是否为空，并且对手机号码进行验证
    if not all([mobile,imagecode,uuid]):
        return jsonify(errno=RET.PARAMERR,errmsg='手机号码格式错误')
    if not re.match(r'^1[345678][0-9]{9}$', mobile):
        return jsonify(errno=RET.PARAMERR, errmsg='手机号码格式错误')
    # 3.获取服务器存储的验证码，uuid为k，进行比较，
    try:
        redis_imagecode = redis_store.get('ImageCode:'+uuid)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询服务器验证码失败')
    # 验证码对比
    if imagecode.lower() != redis_imagecode.lower():
        return jsonify(errno=RET.DATAERR, errmsg='验证码输入有误')
    #判断是否为空或者过期
    if not redis_imagecode:
        return jsonify(errno=RET.NODATA, errmsg='验证码不存在')

    # 4.对比成功，生成短信验证码为字符串
    mobile_code = '%06d' % random.randint(0,999999)
    logging.debug('短信验证码为：' + mobile_code)
    # 6.使用云通讯将短信验证码发送到注册用户手中
    #result = CCP().send_template_sms(mobile,[mobile_code,constants.SMS_CODE_REDIS_EXPIRES/60],'1')
    #if result != 1:
        #return jsonify(errno=RET.THIRDERR, errmsg='发送短信验证码失败')

    # 7.存储短信验证码到redis中:短信验证码在redis中的有效期一定要和短信验证码的提示信息一致
    try:
        redis_store.set('Mobile:' + mobile,mobile_code,constants.SMS_CODE_REDIS_EXPIRES)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='存储短信验证码失败')

    # 8.响应短信发送的结果
    # response = make_response(result)
    return jsonify(errno=RET.OK, errmsg='发送短信验证码成功')

