#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib3
import requests
from utils.decorator_control import Log
from utils.get_authentication_control import Authentication

cookie, token = Authentication().cookie_token


class RestClient:
    """封装api请求类"""

    def __init__(self):
        urllib3.disable_warnings()
        self.sesson = requests.session()  # 创建会话对象
        self.sesson.cookies = cookie
        self._res = None

    @Log(True)
    def request(self, env: set, data=None, json=None, headers=None, **kwargs):
        url, request_method = env
        if request_method == 'get':
            self._res = self.sesson.get(url, headers=headers, **kwargs)
        elif request_method == 'post':
            self._res = self.sesson.post(url, json, data, headers=headers, **kwargs)
        elif request_method == 'options':
            self._res = self.sesson.options(url, **kwargs)
        elif request_method == 'head':
            self._res = self.sesson.head(url, **kwargs)
        elif request_method == 'put':
            self._res = self.sesson.put(url, data, **kwargs)
        elif request_method == 'patch':
            data = json.dump(json) if json else ...
            self._res = self.sesson.patch(url, data, **kwargs)
        elif request_method == 'delete':
            self._res = self.sesson.delete(url, **kwargs)
        return self._res

    @staticmethod
    def headers():
        """全局headers"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'token': token
        }
        return headers


if __name__ == '__main__':
    pass
