#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/4/27 09:51
# @Author : 谈林海
from functools import lru_cache, wraps


def singleton(cls):
    """单例模式装饰器"""

    instances = {}

    @lru_cache(maxsize=None)
    @wraps(cls)
    def wrapper(*args, **kwargs):
        key = (cls, args, frozenset(kwargs.items()))
        if key not in instances:
            instances[key] = cls(*args, **kwargs)
        return instances[key]

    return wrapper