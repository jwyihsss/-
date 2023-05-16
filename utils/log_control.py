#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/3/28 11:24
# @Author : 谈林海
import time
import loguru

from utils.path import root

log_path = root / 'logs'


class Loggings:
    """日志操作方法"""

    def __new__(cls, *args, **kwargs):
        loggers = loguru.logger
        loggers.add(f"{log_path}/log_{time.strftime('%Y_%m_%d')}.log", rotation='1 day', encoding="utf-8",
                    enqueue=True, retention="10 days")
        return loggers


logger = Loggings()

