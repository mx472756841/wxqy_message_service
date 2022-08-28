#!/usr/bin/python3
# -*- coding: utf-8
""" 
@author: mx472756841@gmail.com
@file: wechat.py
@time: 2019/5/8 16:22
"""
import logging

from flask import Blueprint, request, Response, json, current_app

from utils.wechat import WXRequest

wechat_bp = Blueprint('wechat', __name__, url_prefix='/wechat')
logger = logging.getLogger("full_logger")


@wechat_bp.route('/send', methods=['POST'])
def send():
    """
    企业微信发送消息
    @agent_id: 发送消息的企业用用
    @msg_type: 消息类型 text等
    @send_data: 发送消息内容
        Text消息：
            {
                "msg_type": "text",
                "send_data": {
                    "text": {
                        "content": "测试消息"
                    }
                },
                "to_users": ["test"]
            }
        Image消息：
            这种消息需要先上传素材，上传临时素材之后得到MEDIA_ID 可调用wx_req.upload_file
            {
                "msg_type": "image",
                "send_data": {
                    "image": {
                        "media_id": "MEDIA_ID"
                    }
                },
                "to_users": ["test"]
            }
    @to_users: 发送给指定用户
    @to_partys: 发送给指定部门
    @to_tags: 发送给指定标签
    :return:
    """
    try:
        access_token = request.headers.get("AccessToken")
        if access_token not in current_app.config['ACCESS_TOKEN']:
            resp = {
                "code": 98,
                "message": "未经授权的Token"
            }
            return Response(json.dumps(resp), mimetype='application/json')

        req_data = request.json
        # 获取访问微信接口对象
        #: 发送应用ID
        agent_id = req_data.get("agent_id", current_app.config['DEFAULT_WX_AGENT_ID'])
        wx_req = WXRequest.get_request(agent_id)
        msg_type = req_data.get("msg_type")
        send_data = req_data.get("send_data")
        to_users = req_data.get("to_users")
        to_partys = req_data.get("to_partys")
        to_tags = req_data.get("to_tags")
        rs, msg = wx_req.send_msg(agent_id, send_data, msg_type, to_users, to_partys, to_tags)
        resp = {
            "code": 0 if rs else 1,
            "message": msg
        }
        return Response(json.dumps(resp), mimetype='application/json')
    except:
        logger.exception("发送微信通知失败")
        resp = {
            "code": 99,
            "message": "发送微信通知失败"
        }
        return Response(json.dumps(resp), mimetype='application/json')
