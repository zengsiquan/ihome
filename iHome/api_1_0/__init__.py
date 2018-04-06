# -*- coding:utf-8 -*-

from flask import Blueprint
api = Blueprint('api_1_0',__name__,url_prefix='/api/1.0')
from . import verify,passport,profile,house