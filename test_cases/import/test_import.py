#!/usr/bin/env python
# -*- coding: utf-8 -*-
import allure
import pytest


@allure.feature('XXX模块')
@allure.title('XXX接口')
@pytest.mark.imports
@pytest.mark.datafile('test_data/import/test_import.yml')
def test_import(requests, env, headers, case, inputs, expectation, sql, cache):
    print(requests,
          env,
          headers,
          case,
          inputs['file'],
          expectation,
          sql,
          cache)
    res = requests.request(env, headers=headers, files=inputs['file']).json()
    assert res == expectation['response']


