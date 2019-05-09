# wxqy_message_service

## 构建原理
此代码的目的是基于微信提供的企业号，搭建一个实时消息推送平台。
其基本原理：
1. 注册一个微信企业号(免费非认证，微信可提供200个用户使用)
2. 使用者关注企业号，并加入企业微信
3. 微信企业号中创建应用
4. 基于Flask构建一个api平台，并接入微信企业平台，进行消息推送(也可以做其他管理，这里不做延展，只针对实时消息推送)
5. 基于Flask提供的API完成实时消息的推送

## 部署
### virtualenv部署

1. virtualenv -p python3.6 venv
2. . venv/bin/activate
3. pip install -r requirements.txt
4. gunicorn -c etc/gunicorn.py manage:app

### docker部署
这里没有提供docker镜像，可直接使用Dockerfile从本地生成镜像即可
- 生成镜像
```shell
# 在当前目录执行以下命令
docker build -t wxqy_service:latest .
```
- 启动服务

生成镜像之后启动镜像即可
```shell
# ACCESS_TOKEN 简单的鉴权，支持多个，逗号分隔，调用接口时在headers中增加一个Key= AccessToken
docker run -p 10050:5000 -i -t -d \
    --env WX_CORPID=微信企业号ID \
    --env DEFAULT_WX_AGENT_ID=发送消息应用ID \
    --env WX_SECRET=发送消息应用secret \
    --env ACCESS_TOKEN="mSnbqTHqfIG6fIq6,zFIxAxU4wtYKpMzd" \
    --name wxqy_service wxqy_service
```

## 使用
```shell
curl -i -X POST \
    -H 'Content-Type: application/json' \
    -H 'AccessToken: mSnbqTHqfIG6fIq6' \
    --url http://localhost:10050/wechat/send \
    -d '{"msg_type": "text","send_data": {"text": {"content": "测试消息"}},"to_users": ["要发送的用户"]}'
```

