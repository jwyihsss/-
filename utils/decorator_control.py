#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from utils.log_control import logger
from utils.allure_control import ReportStyle


class Log:
    """日志操作装饰器"""

    def __init__(self, switch=True):
        self._switch = switch

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            if self._switch:
                res = func(*args, **kwargs)
                url, method = args[1][:2]
                headers, data, json_data = kwargs.get('headers'), kwargs.get('data'), kwargs.get('json')
                response = res.text
                try:
                    resp = json.loads(response)
                except json.decoder.JSONDecodeError:
                    logger.info('请求返回结果为text类型')
                    resp = res.status_code
                print("\n===============================================================")
                res_info = f"\n请求地址: {url}\n" \
                           f"请求方法: {method.upper()}\n" \
                           f"请求头: {headers}\n" \
                           f"请求数据: {data or json_data}\n" \
                           f"响应数据: {resp}\n" \
                           f"响应耗时(ms): {float(round(res.elapsed.total_seconds() * 1000))}\n" \
                           f"接口响应码: {res.status_code}\n"
                logger.info(res_info)
                ReportStyle.allure_step_no(f"请求地址: {url}")
                ReportStyle.allure_step_no(f"请求方法: {method.upper()}")
                ReportStyle.allure_step("请求头", headers)
                ReportStyle.allure_step("请求数据", data or json_data)
                ReportStyle.allure_step_no(f"接口响应码: {res.status_code}")
                ReportStyle.allure_step_no(f"响应耗时(ms): {round(res.elapsed.total_seconds() * 1000)}")
                ReportStyle.allure_step("响应数据", resp)
                return res
            return func(*args, **kwargs)

        return wrapper
