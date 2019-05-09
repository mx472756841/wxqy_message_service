#!/usr/bin/python3
# -*- coding: utf-8
""" 
@author: mx472756841@gmail.com
@file: log.py
@time: 2019/5/6 14:53
"""
import logging


class InfoFilter(logging.Filter):
    def filter(self, record):
        """
        只筛选出INFO级别的日志
        """
        if logging.INFO <= record.levelno < logging.ERROR:
            return super().filter(record)
        else:
            return False


class ErrorFilter(logging.Filter):
    def filter(self, record):
        """
        只筛选出ERROR级别的日志
        """
        if logging.ERROR <= record.levelno < logging.CRITICAL:
            return super().filter(record)
        else:
            return False


class Log:

    def __init__(self, log_path="/", service_name="default",
                 log_split_type="d", log_split_interval=1,
                 log_backup_count=30):
        self.log_config_dict = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'simple': {
                    'class': 'logging.Formatter',
                    'format': '%(asctime)s %(levelname)s %(name)s %(filename)s %(module)s %(funcName)s '
                              '%(lineno)d %(thread)d %(threadName)s %(process)d %(processName)s %(message)s'
                },
                # json模式, 方便ELK收集处理
                'json': {
                    'class': 'logging.Formatter',
                    'format': '{"time:":"%(asctime)s","level":"%(levelname)s","logger_name":"%(name)s",'
                              '"file_name":"%(filename)s","module":"%(module)s","func_name":"%(funcName)s",'
                              '"line_number":"%(lineno)d","thread_id":"%(thread)d","thread_name":"%(threadName)s",'
                              '"process_id":"%(process)d","process_name":"%(processName)s","message":"%(message)s"}'}
            },
            # 过滤器
            'filters': {
                'info_filter': {
                    '()': InfoFilter
                },
                'error_filter': {
                    '()': ErrorFilter
                }
            },
            # 处理器
            'handlers': {
                # 控制台输出
                'console': {
                    'class': 'logging.StreamHandler',
                    'level': 'INFO',
                    'formatter': 'simple'
                },
                # info文件输出
                'info_file': {
                    'level': 'INFO',
                    'formatter': 'json',
                    'class': 'logging.handlers.TimedRotatingFileHandler',
                    'filename': '{0}/{1}_info.log'.format(log_path, service_name),
                    'when': log_split_type,
                    'interval': log_split_interval,
                    'encoding': 'utf8',
                    'backupCount': log_backup_count,
                    'filters': ['info_filter']
                },
                # error文件输出
                'error_file': {
                    'level': 'ERROR',
                    'formatter': 'json',
                    'class': 'logging.handlers.TimedRotatingFileHandler',
                    'filename': '{0}/{1}_error.log'.format(log_path, service_name),
                    'when': log_split_type,
                    'interval': log_split_interval,
                    'encoding': 'utf8',
                    'backupCount': log_backup_count,
                    'filters': ['error_filter']
                }
            },
            # 记录器
            'loggers': {
                'full_logger': {
                    'handlers': ['console', 'info_file', 'error_file'],
                    'level': 'INFO'
                },
                'only_console_logger': {
                    'handlers': ['console'],
                    'level': 'INFO'
                },
                'only_file_logger': {
                    'handlers': ['info_file', 'error_file']
                }
            }
        }
