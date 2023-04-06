#!/usr/bin/env python
# -*- coding: utf-8 -*-
import allure
import pytest


@allure.feature('登录模块')
@allure.title('登录接口')
@pytest.mark.login
@pytest.mark.datafile('test_data/login/test_login.yml')
def test_login(core, env, case, inputs, expectation):
    res = core.requests.request(env, json=inputs['json'], headers=core.headers).json()
    core.cache.add_cache('test_login', res['key'])
    assert res == expectation['response']
