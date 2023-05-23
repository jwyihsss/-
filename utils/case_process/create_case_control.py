#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/4/24 15:59
# @Author : 谈林海
from pathlib import Path
from typing import List, Dict, Any
import asyncio
import aiofiles

from utils import root
from utils.fake_data.fake_data_control import Mock
from utils.commons.pathlib_control import FileUtils
from utils.read_file_process.read_yaml_control import HandleYaml


class CaseHandler:
    """用例相关数据处理"""

    def __init__(self, file_path: Path = root / 'test_data'):
        """初始化目录路径"""

        self._file_path = file_path

    @property
    def get_data_path(self) -> List[Path]:
        """获取测试数据路径"""

        root_dir = Path(self._file_path)
        data_paths = FileUtils.glob_files(root_dir, '*.yml')
        return data_paths

    @property
    def get_yaml_data(self) -> List[Dict[str, Any]]:
        """获取测试文件对应测试数据"""

        _data_paths = self.get_data_path
        data_list = [HandleYaml(_path).read_yaml() for _path in _data_paths]
        return data_list


class TestCaseAutoCreate(CaseHandler):
    """自动生成测试用例"""

    def __init__(self):
        super().__init__()

    async def generate_test_case(self) -> None:
        """生成测试用例文件"""

        # 遍历测试数据文件
        for file_path, case_detail in zip(self.get_data_path, self.get_yaml_data):
            case_path = Path(str(file_path).replace('test_data', 'test_cases')).parent

            # 处理测试数据
            for data in case_detail.get('tests'):
                params, files, assert_way = data['inputs'].get('params'), data['inputs'].get('file'), data['inputs'].get('assert_way')
                assert_context = {
                    'equal': "(JsonHandler(res).find_one(inputs['assert_key']), expectation['response']) is True",
                    'unequal': "(JsonHandler(res).find_one(inputs['assert_key']), expectation['response']) is True",
                    'in': "(JsonHandler(res).find_one(inputs['assert_key']), expectation['response']) is True",
                    'not_in': "(JsonHandler(res).find_one(inputs['assert_key']), expectation['response']) is True",
                    'true': "(JsonHandler(res).find_one(inputs['assert_key']))",
                    'false': "(JsonHandler(res).find_one(inputs['assert_key']))",
                    'none': "(JsonHandler(res).find_one(inputs['assert_key']) is None)",
                    'not_none': "(JsonHandler(res).find_one(inputs['assert_key']) is not None)"
                }.get(assert_way)

            # 创建目录
            FileUtils.create_dir(case_path) if not FileUtils.is_exist(case_path) else ...
            test_case_path = case_path / f'{file_path.stem}.py'

            # 写入python文件
            if not FileUtils.is_exist(test_case_path):
                async with aiofiles.open(test_case_path, mode='w', encoding="utf8") as file:
                    await file.write(self.case_content(
                        feature=case_path.stem,
                        datafile=f'{file_path.stem}',
                        params=params,
                        files=files,
                        assert_context=assert_context))

    @staticmethod
    def create_case():
        asyncio.run(TestCaseAutoCreate().generate_test_case())

    def case_content(self, feature, datafile, params, files, assert_context):
        """生成测试用例内容"""
        file = "files=input['file'], " if files else ""
        content = f"""#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : {Mock().now_time()}
import allure
import pytest
from utils.read_file_process.json_control import JsonHandler
from utils.case_process.assert_control import Assert


@allure.feature('{feature}')
@pytest.mark.datafile('test_data/{feature}/{datafile}.yml')
def {datafile}(core, env, case, inputs, expectation):
    res = core.requests.request(env, {'data' if params else 'json'}=inputs[{"'params'" if params else "'json'"}], {file}headers=core.headers).json()
    with allure.step('接口响应断言'):
        assert Assert()(inputs['assert_way']){assert_context}"""

        return content


if __name__ == '__main__':
    TestCaseAutoCreate.create_case()
