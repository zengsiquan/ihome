# -*- coding:utf-8 -*-

import redis
class Config(object):
    DEBUG = True
    SECRET_KEY = 'l40oG7xuqCMyNBDE+qfibfk1CYCitMZ7fibPFQBduCZKn22sTzDSP1mUchEMDBPq'


    #配置数据库
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/iHome'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 配置redis
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIME = 3600 * 24

class DevelopmentConfig(Config):
    """创建调试环境下的配置类"""
    pass

class ProductionConfig(Config):
    """创建线上环境下的配置类"""
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@192.168.72.77:3306/iHome'

class UnittestConfig(Config):
    """单元测试的配置:数据库不一致"""
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/iHome_testcast_07'

configs={
    'default_config':Config,
    'development':DevelopmentConfig,
    'production':ProductionConfig,
    'unittest':UnittestConfig
}