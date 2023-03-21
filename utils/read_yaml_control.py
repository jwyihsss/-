#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import yaml
from utils.path import root
from loguru import logger


class HandleYaml:

    def __init__(self, file_path):
        self._file_path = file_path

    def get_yaml_data(self):
        """读取yaml文件数据"""

        if os.path.exists(self._file_path):
            with open(self._file_path, 'r', encoding='utf-8') as data:
                try:
                    res = yaml.safe_load(data)
                except Exception as err:
                    logger.error(f'读取yaml文件失败，请检查内容{err}')
        else:
            raise FileNotFoundError("文件路径不存在，请检查")
        return res

    def add_cache(self, key, val):
        """写入缓存数据"""

        cache_data = self.get_yaml_data() if self.get_yaml_data() else {}
        if cache_data.get('cache') is None:
            cache_data['cache'] = {}
        with open(self._file_path, 'w', encoding='utf-8') as f:
            cache_data['cache'][key] = val
            yaml.dump(cache_data, f, allow_unicode=True)

    def get_cache(self, key):
        try:
            return self.get_yaml_data()['cache'][key]
        except Exception as err:
            logger.error(f'获取缓存失败，请检查{err}')


if __name__ == '__main__':
    print(HandleYaml(root / 'test_data/cache.yml').get_cache('test_courseCreate'))


