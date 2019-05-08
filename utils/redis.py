#!/usr/bin/python3
# -*- coding: utf-8
""" 
@author: mx472756841@gmail.com
@file: redis.py
@time: 2019/5/8 15:48
"""
import os

import redis

from config import config


class RedisClient(object):
    _client = None

    @classmethod
    def _create_redis_client(cls):
        """
        创建连接
        :return:
        """
        config_name = os.getenv('FLASK_CONFIG') or 'default'
        use_config = config[config_name]
        RedisClient._client = redis.StrictRedis(
            use_config.REDIS_HOST, use_config.REDIS_PORT,
            use_config.REDIS_DB, use_config.REDIS_PASS
        )

    @classmethod
    def get_client(cls):
        if RedisClient._client is None:
            cls._create_redis_client()
        return RedisClient._client
