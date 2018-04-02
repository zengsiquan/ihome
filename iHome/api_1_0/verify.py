# -*- coding:utf-8 -*-

from . import api
from iHome.utils.captcha.captcha import captcha
from flask import request,abort,jsonify,make_response
from iHome import constants
from iHome import redis_store
from iHome.utils.response_code import RET

@api.route('/image_code')
def get_image_code():
    uuid = request.args.get('uuid')
    print(uuid)
    last_uuid = request.args.get('last_uuid')
    print(last_uuid)
    if not uuid:
        abort(403)
    name,text,image = captcha.generate_captcha()
    try:
        if last_uuid:

            redis_store.delete('ImageCode:'+last_uuid)


        redis_store.set('ImageCode:'+uuid,text,constants.IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        print e
        # restful要求返回响应状态
        return jsonify(errno=RET.DBERR,errmsg=u'保存验证码失败')
        # 4.返回图片验证码
    resposne = make_response(image)
    resposne.headers['Content-Type'] = 'image/jpg'
    return resposne
