#!/usr/bin/env python
# -*- coding: utf-8 -*-
from utils import config
from jsonpath import jsonpath


class Authentication:
    """获取token/cookies"""

    def __init__(self):
        self.payload = {"account": config.account,
                        "password": config.password,
                        "isVaildCode": False}

    @property
    def cookie_token(self):
        import requests
        res = requests.post('https://tianqiapi/login', data=self.payload)
        res_cookies, res_token = res.cookies, jsonpath(res.json(), '$..token')[0]
        return res_cookies, res_token


# cookies, token = Authentication().cookie_token
