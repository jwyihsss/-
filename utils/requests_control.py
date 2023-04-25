#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/4/24 15:59
# @Author : 谈林海
import urllib3
from urllib3.util.retry import Retry
import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import RetryError, Timeout, RequestException

from utils import config
from utils.json_control import JsonHandler
from utils.log_control import logger, Log
from utils.create_cookie_control import Cookies


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


session = requests.session()
session.verify = False
session.cookies, token = Authentication().cookie_token


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
        self.session = session  # 创建会话对象
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

    @Log(True)
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
            # 'token': token
        }
        return headers


if __name__ == '__main__':
    pass
