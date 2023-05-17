#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/4/24 15:59
# @Author : 谈林海
import json
import urllib3
from urllib3.util.retry import Retry
import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import RetryError, Timeout, RequestException
from functools import wraps

from utils import *
from utils.read_file_process.json_control import JsonHandler
from utils.requests_process.create_cookie_control import Cookies
from utils.commons.allure_control import ReportStyle


class Authentication:
    """获取token/cookies"""

    def __init__(self):
        # 读取全局配置中的账号信息
        self.payload = {"account": config.account,
                        "password": config.password
                        }

    @property
    def cookie_token(self):
        try:
            res = requests.post('https://tianqiai/login', data=self.payload)
            js = JsonHandler(res.json())
            res_cookies, res_token = res.cookies, js.find_one('$..token')
            return res_cookies, res_token
        except Exception as err:
            logger.warning(f'未获取到登录认证信息，请检查: {err}')
            return Cookies, {}  # 如果cookie没有获取成功，则根据全局配置域名生成一个备用cookie


class RestClient:
    """封装api请求类"""

    def __init__(self,
                 timeout=10,
                 retry=3,
                 backoff_factor=0.3,
                 proxies=None
                 ):
        # 初始化函数，设置请求超时时间、重试次数、backoff因子（指定失败后下一次重试时间间隔的增长因子）、代理等参数
        # 这四个参数都是默认设置的，用户可以根据需要进行更改
        urllib3.disable_warnings()
        self.timeout = timeout  # 超时时间
        self.proxies = proxies or {}  # 设置代理
        self.session = requests.session()  # 创建会话对象
        self.session.Timeout = Timeout(timeout)  # 设置超时时间
        self.session.verify = False
        self.session.cookies, self.token = Authentication().cookie_token
        self.session.proxies.update(self.proxies)

        retry_strategy = Retry(
            total=retry,
            backoff_factor=backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        # 设置重试策略并将其与会话对象关联，以便每次请求失败时自动重试

    def res_log(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
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
            return res.status_code if isinstance(resp, int) else res
        return wrapper

    @res_log
    def request(self, env, **kwargs):
        url, request_method = env
        res = {
            'get': lambda: self.session.get(url, **kwargs),
            'post': lambda: self.session.post(url, **kwargs),
            'options': lambda: self.session.options(url, **kwargs),
            'head': lambda: self.session.head(url, **kwargs),
            'put': lambda: self.session.put(url, **kwargs),
            'patch': lambda: self.session.patch(url, **kwargs),
            'delete': lambda: self.session.delete(url, **kwargs)
        }.get(request_method.lower(), False)()

        try:
            return res
        except (RequestException, Timeout, RetryError) as err:
            logger.error(f'请求失败: {err}')
            return None

    @staticmethod
    def headers():
        """全局headers"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
            # 'token': self.token
        }
        return headers

    res_log = staticmethod(res_log)

