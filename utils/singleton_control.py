#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/4/27 09:51
# @Author : 谈林海


class SingletonPattern:
    """单例模式装饰器"""

    def __init__(self, cls):
        self.cls = cls
        self._instance = None

    def __call__(self, *args, **kwargs):
        if not self._instance:
            self._instance = self.cls(*args, **kwargs)
        return self._instance