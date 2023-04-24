#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023-04-24 17:07:07
import allure
import pytest


@allure.feature('XXX模块')
@allure.title('XXX接口')
@pytest.mark.imports
@pytest.mark.datafile('test_data/imports/test_imports.yml')
def test_imports(core, env, case, inputs, expectation):
    # core.requests: 返回请求方法对象
    # core.headers: 返回全局请求头
    # core.sql: 返回查询方法对象
    # core.cache: 返回缓存处理方法对象
    res = core.requests.request(env, data=inputs['json'], headers=core.headers, files=inputs['file']).json()
    assert res == expectation['response']