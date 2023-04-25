#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/4/10 10:56
# @Author : 谈林海
from jsonpath import jsonpath


class JsonHandler:

    def __init__(self, obj):
        """
        初始化 JsonPathFinder 类，传入需要查找的 JSON 对象
        """
        self.obj = obj

    def find_one(self, expr):
        """
        查找 JSON 对象中符合指定表达式的第一个节点
        """
        result = jsonpath(self.obj, expr)
        return result[0] if result else None

    def find_all(self, expr):
        """
        查找 JSON 对象中符合指定表达式的所有节点
        """
        return jsonpath(self.obj, expr)

    def find_first(self, *exprs):
        """
        按顺序查询 JSON 对象中第一个存在的节点
        """
        for expr in exprs:
            result = self.find_one(expr)
            if result:
                return result
        return None

    def find_default(self, default, *exprs):
        """
        按顺序查询 JSON 对象中第一个存在的节点，如果不存在则返回默认值
        """
        result = self.find_first(*exprs)
        return result if result is not None else default


if __name__ == '__main__':
    pass