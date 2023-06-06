#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/4/27 09:51
# @Author : 谈林海
from functools import lru_cache


def singleton(cls):
    """单例模式装饰器"""
    instances = {}

    @lru_cache(maxsize=None)
    def get_instance(*args, **kwargs):
        key = (cls, args, tuple(sorted(kwargs.items())))
        if key not in instances:
            instances[key] = cls(*args, **kwargs)
        return instances[key]

    return get_instance