#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pytest
from utils.allure_control import ReportStyle
from utils.path import root
from utils.read_yaml_control import HandleYaml
from utils.data_handle_control import DataHandler, Config
from utils.requests_control import RestClient


def pytest_generate_tests(metafunc):
    """参数化测试函数"""

    test_cases = []
    markers = metafunc.definition.own_markers
    for marker in markers:
        if marker.name == 'datafile':
            test_data_path = os.path.join(metafunc.config.rootdir, marker.args[0]) if marker.args else ...
            test_data = HandleYaml(test_data_path).read_yaml()
            for data in test_data['tests']:
                if data['inputs'].get('file', {}):
                    data['inputs']['file'] = {'file': (
                        data['inputs']['file'], open(root / f"files/{data['inputs']['file']}", 'rb'),
                        'application/json')}
                    test_case = {
                        'case': data.get('case', {}),
                        'env': (str(host()) + str(test_data['common_inputs'].get('path', {})),
                                str(test_data['common_inputs'].get('method', ''))),
                        'inputs': data.get('inputs', {}),
                        'expectation': data.get('expectation', {})
                    }
                test_cases.append(test_case)

            metafunc.parametrize(
                "env, case, inputs, expectation",
                [(tc['env'], tc['case'], tc['inputs'], tc['expectation']) for tc in test_cases],
                scope='function'
            )


@pytest.fixture(scope='function', autouse=True)
def alert_inputs(request):
    """替换inputs中的参数化数据"""

    if 'inputs' in request.fixturenames:
        inputs = request.getfixturevalue('inputs')
        DataHandler(config=Config()).replace_values(inputs['json'])


@pytest.hookimpl
def pytest_assertion_pass(item, lineno, orig, expr=None, values=None):
    ReportStyle.allure_step_no(f'断言通过:  {orig}')


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

    res_host = HandleYaml(root / 'config.yml').read_yaml()['host']
    return res_host


@pytest.fixture()
def requests():
    """返回实例化请求方法"""

    yield RestClient()


@pytest.fixture()
def sql():
    """返回实例化数据库方法"""

    from utils.database_control import MysqlDB
    with MysqlDB() as sql:
        yield sql


@pytest.fixture(scope='session')
def cache():
    """返回一个字典，用作数据共享"""

    yield {}
