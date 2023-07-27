#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023-04-25 11:52:55
import json

import allure
import pytest
import time  # 添加时间模块

@allure.feature('登录模块')
@allure.title('登录接口')
@pytest.mark.login
@allure.feature('login')
@pytest.mark.datafile('test_data/login/test_login.yml')
def test_tianqi(core, env, case, inputs, expectation):
    # 添加时间戳到请求头
    timestamp = int(time.time()*1000)
    core.headers['x-k7-timestamp'] = str(timestamp)
    core.headers['Content-Type']='application/json;charset=UTF-8'

    res = core.requests.request(env, data=json.dumps(inputs['data']), headers=core.headers).json()
    core.cache.add_cache('test_login', res)
    assert res == expectation
