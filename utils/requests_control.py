#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib3
import requests
from loguru import logger
from utils.decorator_control import Log
from utils.get_authentication_control import Authentication

# cookie, token = Authentication().cookie_token
session = requests.session()
session.verify = False
# session.cookies = cookie


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
