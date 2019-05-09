#!/bin/sh

# 启动redis-server
redis-server &

gunicorn -c etc/gunicorn.py manage:app



