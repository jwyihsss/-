#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/4/24 11:12
# @Author : 谈林海
import json
from pathlib import Path
from utils.path import root
from utils.log_control import logger
from utils.fake_data_control import Mock
from utils.clean_file_control import CleanFile
from utils.read_yaml_control import HandleYaml


class TestCaseAutoCreate:
    """自动创建测试用例"""

    def __init__(self, file_path=root / 'test_data'):
        """初始化目录路径"""

        self._file_path = file_path
        CleanFile(root / 'test_cases')()

    @property
    def get_data_path(self):
        """获取测试数据路径及转换为测试用例路径"""

        root_dir = Path(self._file_path)
        data_paths = [_path for _path in root_dir.rglob('*.yml') if
                      _path.is_file() and _path.name != 'cache.yml']
        case_paths = [Path(str(_path).replace('test_data', 'test_cases')).parent for _path in root_dir.rglob('*.yml') if
                      _path.is_file() and _path.name != 'cache.yml']
        return data_paths, case_paths

    @property
    def get_yaml_data(self):
        """获取测试文件对应测试数据"""

        _data_paths = self.get_data_path[0]
        data_list = [HandleYaml(_path).read_yaml() for _path in _data_paths]
        # data_dict = {k: v for k, v in zip(_data_paths, data_list)}
        return data_list

    def get_case_model(self, case_path):
        """获取测试数据所属模块"""

        case_paths = Path(case_path).parents[0]
        return case_paths

    @property
    def generate_case_model(self):
        """生成测试用例模块"""

        case_list = list(map(self.get_case_model, self.get_data_path[1]))
        return case_list

    @property
    def generate_case_name(self):
        """生成测试用例名称"""

        return [case_path.stem for case_path in self.get_data_path[1]]

    def generate_test_case(self):
        """生成测试用例文件"""

        data_dict = {k: v for k, v in zip(self.get_data_path[1], self.get_yaml_data)}
        for file_path, case_detail in data_dict.items():
            file_name = str(file_path).split('/')[-1]
            for data in case_detail.get('tests'):
                params = data['inputs'].get('params')
                jsons = data['inputs'].get('json')
                sql = data['inputs'].get('sql')
            file_path.mkdir(parents=True, exist_ok=True)  # 先创建目录
            case_path = file_path / f'test_{file_name}.py'
            feature = str(file_name).split('_')[-1]
            with case_path.open(mode='w', encoding='utf-8') as f:
                f.write(self.case_content(feature, file_name, params, jsons, sql))  # 覆盖写入python文件

    def case_content(self, feature, datafile, params, jsons, sql):
        """生成测试用例内容"""

        content = f"""#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : {Mock().now_time()}
import allure
import pytest
from utils.json_control import get_json
from utils.assert_control import Assert


@allure.feature('{feature}')
@pytest.mark.datafile('test_data/{feature}/{datafile}.yml')
def test_tianqi(core, env, case, inputs, expectation):
    res = core.requests.request(env, {'data' if params else 'json'}=inputs[{"'params'" if params else "'json'"}], headers=core.headers).json()
    assert Assert(get_json(res, inputs['assert_key']), expectation['response']).ass(inputs['assert_way']) is True"""

        return content


if __name__ == '__main__':
    TestCaseAutoCreate().generate_test_case()
