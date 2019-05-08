#!/usr/bin/python3
# -*- coding: utf-8
""" 
@author: mx472756841@gmail.com
@file: base.py
@time: 2019/5/8 11:03
@desc: 基类
"""
import requests
from flask import json


class BaseRequest(object):
    def _request(self, method, url, **kwargs):
        headers = {}
        if not kwargs.get('files'):
            headers["Content-Type"] = "application/json;charset=UTF-8"
        if not kwargs.get('verify'):
            # 如果没有指定，默认不验证证书
            kwargs['verify'] = False
        data = kwargs.get('data')
        if isinstance(data, dict):
            data = json.dumps(data)
            kwargs['data'] = data
        headers.update(kwargs.get("headers") or {})
        kwargs['headers'] = headers
        try:
            response = requests.request(method, url=url, **kwargs)
        except ConnectionError as ex:
            return {"message": ex}, 500
        except requests.ReadTimeout as ex:
            return {"message": ex}, 500
        except Exception as ex:
            return {"message": ex}, 500
        else:
            try:
                res = response.json()
            except:
                res = {}
            return res, response.status_code

    def req_get(self, url, data=None, **kwargs):
        return self._request("GET", url, data=data, **kwargs)

    def req_post(self, url, data=None, **kwargs):
        return self._request("POST", url, data=data, **kwargs)

    def req_put(self, url, data=None, **kwargs):
        return self._request("PUT", url, data=data, **kwargs)

    def req_del(self, url, data=None, **kwargs):
        return self._request("DELETE", url, data=data, **kwargs)
