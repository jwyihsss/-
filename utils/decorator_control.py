#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from loguru import logger
from utils.allure_control import ReportStyle


class Log:
    """日志操作装饰器"""

    def __init__(self, switch=True):
        self._switch = switch

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            if self._switch is True:
                res = func(*args, **kwargs)
                _url = args[1] if args[1] else {}
                _method = args[2] if args[2] else {}
                if _method == 'post':
                    _headers = args[5] if args[5] else {}
                    _data = args[3] if args[3] else {}
                    _json = args[4] if args[4] else {}
                elif _method == 'get':
                    _headers = args[3] if args[3] else {}
                    _data = kwargs if kwargs else {}
                    _json = kwargs if kwargs else {}
                r = res.text
                try:
                    resp = json.loads(r)
                except json.decoder.JSONDecodeError:
                    logger.info(f'请求返回结果为text')
                    resp = res.status_code
                logger.info("\n===============================================================")
                res_info = f"请求地址: {_url}\n" \
                           f"请求方法: {_method.upper()}\n" \
                           f"请求头: {_headers}\n" \
                           f"请求数据: {_data if _data else _json}\n\n" \
                           f"响应数据: {resp}\n" \
                           f"响应耗时(ms): {float(round(res.elapsed.total_seconds() * 1000))}\n" \
                           f"接口响应码: {res.status_code}"
                logger.info(res_info)
                ReportStyle.allure_step_no(f"请求地址: {_url}")
                ReportStyle.allure_step_no(f"请求方法: {_method.upper()}")
                ReportStyle.allure_step("请求头", _headers)
                ReportStyle.allure_step("请求数据", _data if _data else _json)
                ReportStyle.allure_step_no(f"接口响应码: {res.status_code}")
                ReportStyle.allure_step_no(f"响应耗时(ms): {round(res.elapsed.total_seconds() * 1000)}")
                ReportStyle.allure_step("响应数据", resp)
            return res
        return wrapper
