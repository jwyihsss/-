#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inspect
from faker import Faker
from utils.log_control import logger
from datetime import datetime

faker = Faker(locale='zh_CN')


class Mock:
    """ Mock数据 """
    def __init__(self, func_name=None):
        self._faker = faker
        self.func_name = func_name
        self.func_map = self.func_list()

    def __call__(self, *args, **kwargs):
        if self.func_map.get(self.func_name, False):
            return getattr(self, str(self.func_map.get(self.func_name)))()
        else:
            func_name = self.func_name[:self.func_name.find('(')]
            args_str = self.func_name[self.func_name.find('(') + 1:self.func_name.find(')')]
            if func_name in dir(self._faker):
                func = getattr(self._faker, func_name)
                params = inspect.signature(func).parameters
                params_list = [name for name, param in params.items()]
                if len(params_list) == 0 or len(args_str) == 0:
                    return func()
                else:
                    return func(*eval(args_str))
            else:
                logger.error(f"未获取到对应方法，请检查")

    def func_list(self):
        """
        :return: 返回除内置方法外类中的所有其他方法
        """
        all_methods = inspect.getmembers(self, inspect.ismethod)
        func_list = {name: (name if not str(name).startswith('__') else '...') for name, method in all_methods}
        return func_list

    def now_time(self):
        """
        计算当前时间
        :return:
        """
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return now_time

    def now_time_stamp(self):
        """
        计算当前时间戳(秒级)
        :return:
        """
        now_time_stamp = datetime.now().timestamp()
        return int(now_time_stamp)


if __name__ == '__main__':
    r1 = Mock('random_int')()
    r2 = Mock('random_int(1, 99)')()
    r3 = Mock().now_time()
    print(r1)
    print(Mock('phone_number()')())

