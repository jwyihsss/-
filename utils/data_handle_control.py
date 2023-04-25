#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pathlib import Path
from pydantic import BaseModel
from typing import Any, Dict, Union

from utils.path import root
from utils.fake_data_control import Mock
from utils.read_yaml_control import HandleYaml


class Config(BaseModel):
    """定义配置类"""

    cache_path: Union[str, Path] = root / 'test_data/cache.yaml'


class DataHandler:
    def __init__(self, config: Config):
        self.config = config
        self.cache_data = self.load_cache()

    def load_cache(self) -> Dict[str, Any]:
        """加载缓存数据"""

        cache_path = Path(self.config.cache_path)
        return HandleYaml(cache_path).read_yaml().get('cache', {})

    def replace_values(self, data):
        """ 替换字典中指定格式的字符串值 """

        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    self.replace_values(value)
                elif isinstance(value,
                                str) and '{{' in value and '}}' in value and 'int.' not in value and 'str.' not in value:
                    func = value[value.find('{') + 2:value.find('}')]
                    data[key] = data[key].replace('{{%s}}' % f'{func}', str(Mock(func)()))
                elif isinstance(value, str) and '$cache.' in value:
                    cache_name = value[value.find('.') + 1:]
                    data[key] = self.cache_data.get(cache_name, None)
                elif isinstance(value, str) and 'int.' in value:
                    func = value[value.find('{') + 2:value.find('}')]
                    data[key] = int(data[key].replace('{{%s}}' % f'{func}', str(Mock(func[func.find('.') + 1:])())))
                elif isinstance(value, str) and 'str.' in value:
                    func = value[value.find('{') + 2:value.find('}')]
                    data[key] = str(data[key].replace('{{%s}}' % f'{func}', str(Mock(func[func.find('.') + 1:])())))
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, (dict, list)):
                    self.replace_values(item)
                elif isinstance(item,
                                str) and '{{' in item and '}}' in item and 'str.' not in item and 'int.' not in item:
                    func = item[item.find('{') + 2:item.find('}')]
                    data[data.index(item)] = data[data.index(item)].replace('{{%s}}' % f'{func}', str(Mock(func)()))
                elif isinstance(item, str) and '$cache.' in item:
                    cache_name = item[item.find('.') + 1:]
                    data[data.index(item)] = self.cache_data.get(cache_name, None)
                elif isinstance(item, str) and 'int.' in item:
                    func = item[item.find('{') + 2:item.find('}')]
                    data[data.index(item)] = int(
                        data[data.index(item)].replace('{{%s}}' % f'{func}', str(Mock(func[func.find('.') + 1:])())))
                elif isinstance(item, str) and 'str.' in item:
                    func = item[item.find('{') + 2:item.find('}')]
                    data[data.index(item)] = str(
                        data[data.index(item)].replace('{{%s}}' % f'{func}', str(Mock(func[func.find('.') + 1:])())))
        return data


if __name__ == '__main__':
    pass
