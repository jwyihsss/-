#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/4/24 15:59
# @Author : 谈林海
from pathlib import Path
from typing import List, Dict, Any, Tuple

from utils.log_control import logger
from utils.path import root
from utils.fake_data_control import Mock
from utils.pathlib_control import FileUtils
from utils.read_yaml_control import HandleYaml


class CaseHandler:
    """用例相关数据处理"""

    def __init__(self, file_path: Path = root / 'test_data'):
        """初始化目录路径"""

        self._file_path = file_path

    @property
    def get_data_path(self) -> Tuple[List[Path], List[Path]]:
        """获取测试数据路径及转换为测试用例路径"""

        root_dir = Path(self._file_path)
        # 获取所有 yml 格式的测试数据文件路径
        data_paths = FileUtils.glob_files(root / 'test_data', '*.yml')
        # 将测试数据文件路径转换为对应的测试用例路径
        case_paths = [Path(str(_path).replace('test_data', 'test_cases')).parent for _path in root_dir.rglob('*.yml') if
                      _path.is_file() and _path.name != 'cache.yaml']
        return data_paths, case_paths

    @property
    def get_yaml_data(self) -> List[Dict[str, Any]]:
        """获取测试文件对应测试数据"""

        _data_paths = self.get_data_path[0]
        data_list = [HandleYaml(_path).read_yaml() for _path in _data_paths]
        return data_list

    def get_case_model(self, case_path: Path) -> Path:
        """获取测试数据所属模块"""

        case_paths = Path(case_path).parents[0]
        return case_paths

    @property
    def generate_case_model(self) -> List[Path]:
        """生成测试用例模块"""

        case_list = list(map(self.get_case_model, self.get_data_path[1]))
        return case_list

    @property
    def generate_case_name(self) -> List[str]:
        """生成测试用例名称"""

        return [case_path.stem for case_path in self.get_data_path[1]]


class TestCaseAutoCreate(CaseHandler):
    """自动生成测试用例"""

    def __init__(self):
        super().__init__()

    def generate_test_case(self) -> None:
        """生成测试用例文件"""

        data_dict = {k: v for k, v in zip(self.get_data_path[1], self.get_yaml_data)}
        for file_path, case_detail in data_dict.items():
            for data in case_detail.get('tests'):
                params, files = data['inputs'].get('params'), data['inputs'].get('file')
            logger.info(f'{file_path}目录已存在, 跳过创建') if FileUtils.is_exist(file_path) else FileUtils.create_dir(file_path)  # 创建目录
            case_path = file_path / f'test_{file_path.stem}.py'
            if not FileUtils.is_exist(case_path):
                FileUtils.write_file(case_path, content=self.case_content(
                    file_path.stem,
                    f'test_{file_path.stem}',
                    params,
                    files
                ))  # 写入python文件

    def case_content(self, feature, datafile, params, files):
        """生成测试用例内容"""
        if files:
            file = "files=input['file'], "
        else:
            file = ""
        content = f"""#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : {Mock().now_time()}
import allure
import pytest
from utils.json_control import JsonHandler
from utils.assert_control import Assert


@allure.feature('{feature}')
@pytest.mark.datafile('test_data/{feature}/{datafile}.yml')
def test_tianqi(core, env, case, inputs, expectation):
    res = core.requests.request(env, {'data' if params else 'json'}=inputs[{"'params'" if params else "'json'"}], {file}headers=core.headers).json()
    assert Assert(JsonHandler(res).find_one(inputs['assert_key']), expectation['response']).ast(inputs['assert_way']) is True"""

        return content


if __name__ == '__main__':
    TestCaseAutoCreate().generate_test_case()
