#!/usr/bin/env python
# -*- coding: utf-8 -*-
from utils.path import root
from jsonpath import jsonpath
from utils.read_yaml_control import HandleYaml


class Authentication:
    """获取token/cookies"""

    def __init__(self):
        self.handle_yaml = HandleYaml(root / 'config.yml')
        self.payload = {"account": self.handle_yaml.get_yaml_data()['account'],
                        "password": self.handle_yaml.get_yaml_data()['password'],
                        "isVaildCode": False}

    @property
    def cookie_token(self):
        import requests
        res = requests.post('https://tianqiapi/login', data=self.payload)
        res_cookies, res_token = res.cookies, jsonpath(res.json(), '$..token')[0]
        return res_cookies, res_token


cookies, token = Authentication().cookie_token
