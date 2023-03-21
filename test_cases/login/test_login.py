#!/usr/bin/env python
# -*- coding: utf-8 -*-
import allure
import pytest


@allure.feature('登录模块')
@allure.title('登录接口')
@pytest.mark.login
@pytest.mark.datafile('test_data/login/test_login.yml')
def test_login(requests, env, headers, case, inputs, expectation, cache):
    res = requests.request(env, json=inputs['json'], headers=headers).json()
    cache.add_cache('test_login', res['key'])
    assert res == expectation['response']
