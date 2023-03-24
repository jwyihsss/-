#!/usr/bin/env python
# -*- coding: utf-8 -*-
import yaml
from utils.path import root
from loguru import logger


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
        cache_data = data.get('cache', {})
        cache_data[key] = val
        data['cache'] = cache_data
        self._write_yaml(data)

    def get_cache(self, key):
        data = self.read_yaml()
        return data.get('cache', {}).get(key)


if __name__ == '__main__':
    print(HandleYaml(root / 'test_data/cache.yml').get_cache('test_courseCreate'))


