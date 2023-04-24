#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023-04-24 17:07:07
import allure
import pytest
from utils.json_control import get_json
from utils.assert_control import Assert


@allure.feature('tianqi')
@pytest.mark.datafile('test_data/tianqi/test_tianqi.yml')
def test_tianqi(core, env, case, inputs, expectation):
    res = core.requests.request(env, data=inputs['json'], headers=core.headers).json()
    assert Assert(get_json(res, inputs['assert_key']), expectation['response']).ass(inputs['assert_way']) is True