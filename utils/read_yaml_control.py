#!/usr/bin/env python
# -*- coding: utf-8 -*-
import yaml
from utils.log_control import logger


class HandleYaml:
    """操作yaml文件"""

    def __init__(self, file_path):
        """初始化文件路径"""

        self._file_path = file_path

    def read_yaml(self):
        """读取yaml文件"""

        try:
            with open(self._file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            logger.error("文件路径不存在，请检查")
            raise

    def _write_yaml(self, data):
        """写入yaml文件"""

        with open(self._file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True)

    def add_cache(self, key, val):
        """写入缓存数据"""
        data = self.read_yaml()
        data['cache'] = {**data.get('cache', {}), key: val}
        self._write_yaml(data)


if __name__ == '__main__':
    HandleYaml('/Users/tanlinhai/PythonProjects/t2-api-autotest/test_data/tianqi/test_tianqi.yml').read_yaml()
