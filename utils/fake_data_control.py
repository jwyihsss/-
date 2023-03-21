#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inspect
import random
from faker import Faker
from loguru import logger
from datetime import datetime


class Execute:
    """ Mock数据 """

    def __init__(self, func_name):
        self.faker = Faker(locale='zh_CN')
        self.func_name = func_name
        self.func_map = self.func_list()

    def __call__(self, *args, **kwargs):
        func = self.func_map.get(self.func_name, None)
        if func is not None and callable(func):
            return func()
        else:
            logger.error("未获取到该字段对应方法，请检查")

    def func_list(self):
        """
        :return: 返回除内置方法外类中的所有其他方法
        """
        func_list = {}
        all_method = inspect.getmembers(self, inspect.ismethod)
        for name in all_method:
            func_list[name[0]] = eval(f'self.{name[0]}') if '__' not in str(name[0]) else ...
        return func_list

    def random_int(self):
        """
        :return: 随机数
        """
        _data = random.randint(0, 5000)
        return _data

    def random_phone(self):
        """
        :return: 随机生成手机号码
        """
        return '1140124' + str(self.faker.phone_number()[7:])

    def random_id_number(self):
        """

        :return: 随机生成身份证号码
        """

        id_number = self.faker.ssn()
        return id_number

    def random_female_name(self):
        """

        :return: 女生姓名
        """
        female_name = self.faker.name_female()
        return female_name

    def random_male_name(self):
        """

        :return: 男生姓名
        """
        male_name = self.faker.name_male()
        return male_name

    def random_email(self):
        """

        :return: 生成邮箱
        """
        email = self.faker.email()
        return email

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

    def random_num(self):
        """

        :return: 随机1~10数字
        """
        num = random.randint(1, 10)
        return num


if __name__ == '__main__':
    r = Execute('random_num')()
    print(r)
