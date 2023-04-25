#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023-04-25 11:52:55
import allure
import pytest


@allure.feature('登录模块')
@allure.title('登录接口')
@pytest.mark.login
@allure.feature('login')
@pytest.mark.datafile('test_data/login/test_login.yml')
def test_tianqi(core, env, case, inputs, expectation):
    res = core.requests.request(env, data=inputs['params'], headers=core.headers).json()
    core.cache.add_cache('test_login', res['key'])
    assert res == expectation['response']