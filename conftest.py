#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pytest
from utils.path import root
from itertools import zip_longest
from utils.database_control import MysqlDB
from utils.fake_data_control import Execute
from utils.requests_control import RestClient
from utils.open_file_control import open_file
from utils.read_yaml_control import HandleYaml


def replace_cache_values(data):
    """ 替换字典中所有包含"$cache" 和 "{{}}" 格式的字符串值 """

    cache_data = HandleYaml(root / 'test_data/cache.yml').get_yaml_data()
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict) or isinstance(value, list):
                replace_cache_values(value)
            elif isinstance(value, str) and '{{' in value and '}}' in value:
                func = value[value.find('{') + 2:value.find('}')]
                data[key] = data[key].replace('{{%s}}' % f'{func}', str(Execute(func)()))
            elif isinstance(value, str) and '$cache' in value:
                cache_name = value[value.find('.') + 1:]
                data[key] = cache_data['cache'].get(cache_name, None)
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict) or isinstance(item, list):
                replace_cache_values(item)
            elif isinstance(item, str) and '{{' in item and '}}' in item:
                func = item[item.find('{') + 2:item.find('}')]
                data[data.index(item)] = data[data.index(item)].replace('{{%s}}' % f'{func}', str(Execute(func)()))
            elif isinstance(item, str) and '$cache' in item:
                cache_name = item[item.find('.') + 1:]
                data[data.index(item)] = cache_data['cache'].get(cache_name, None)
    return data


@pytest.fixture(scope='function', autouse=True)
def alert_inputs(request):
    """替换inputs中的参数化数据"""

    if 'inputs' in request.fixturenames:
        inputs = request.getfixturevalue('inputs')
        replace_cache_values(inputs['json'])


def replace_cache_values(data):
    """ 替换字典中所有包含"$cache" 和 "{{}}" 格式的字符串值 """

    cache_data = HandleYaml(root / 'test_data/cache.yml').get_yaml_data()
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict) or isinstance(value, list):
                replace_cache_values(value)
            elif isinstance(value, str) and '{{' in value and '}}' in value:
                func = value[value.find('{') + 2:value.find('}')]
                data[key] = data[key].replace('{{%s}}' % f'{func}', Execute(func)())
            elif isinstance(value, str) and '$cache' in value:
                cache_name = value[value.find('.') + 1:]
                data[key] = cache_data['cache'].get(cache_name, None)
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict) or isinstance(item, list):
                replace_cache_values(item)
            elif isinstance(item, str) and '{{' in item and '}}' in item:
                func = item[item.find('{') + 2:item.find('}')]
                data[data.index(item)] = data[data.index(item)].replace('{{%s}}' % f'{func}', Execute(func)())
            elif isinstance(item, str) and '$cache' in item:
                cache_name = item[item.find('.') + 1:]
                data[data.index(item)] = cache_data['cache'].get(cache_name, None)
    return data


# def assert_with_attachment(assert_msg=None, result=None):
#     with allure.step(assert_msg):
#         try:
#             assert result
#         except AssertionError:
#             allure.attach(str(result), name="断言失败", attachment_type=AttachmentType.TEXT)
#             raise
#         else:
#             allure.attach(str(result), name="断言通过", attachment_type=AttachmentType.TEXT)


def pytest_collection_modifyitems(items):
    """测试用例收集完成时，将收集到的item的name和nodeid的中文显示"""

    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")


@pytest.fixture()
def headers():
    """通用请求头"""

    yield RestClient().headers()


def host():
    """获取配置文件中的域名"""

    res_host = HandleYaml(root / 'config.yml').get_yaml_data()['host']
    return res_host


@pytest.fixture()
def requests():
    """返回实例化请求方法"""

    yield RestClient()


@pytest.fixture()
def sql():
    """返回实例化数据库方法"""

    yield MysqlDB()


@pytest.fixture(scope='session')
def cache():
    """返回一个字典，用作数据共享"""

    yield {}
