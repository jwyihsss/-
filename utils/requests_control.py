#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib3
import requests
from loguru import logger
from jsonpath import jsonpath

from utils.decorator_control import Log
from utils import config
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
            res_cookies, res_token = res.cookies, jsonpath(res.json(), '$..token')[0]
            return res_cookies, res_token
        except Exception as err:
            logger.error(f'获取认证信息失败，请检查: {err}')
            return Cookies, {}  # 如果cookie没有获取成功，则根据全局配置域名生成一个备用cookie


session = requests.session()
session.verify = False
session.cookies, token = Authentication().cookie_token


class RestClient:
    """封装api请求类"""

    def __init__(self):
        urllib3.disable_warnings()
        self.session = session  # 创建会话对象

    @Log(True)
    def request(self, env, data=None, json=None, headers=None, **kwargs):
        url, request_method = env
        res = {
            'get': lambda: self.session.get(url, headers=headers, **kwargs),
            'post': lambda: self.session.post(url, json, data, headers=headers, **kwargs),
            'options': lambda: self.session.options(url, **kwargs),
            'head': lambda: self.session.head(url, **kwargs),
            'put': lambda: self.session.put(url, data, **kwargs),
            'patch': lambda: self.session.patch(url, json=json.dump(json) if json else ..., **kwargs),
            'delete': lambda: self.session.delete(url, **kwargs)
        }.get(request_method.lower(), False)()

        return res if res else logger.error('不存在的请求方式，请检查')

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
