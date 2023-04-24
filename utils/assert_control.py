#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/4/24 15:59
# @Author : 谈林海
from utils.log_control import logger


class Assert:
    def __init__(self, excp, resp):
        self._excp = excp
        self._resp = resp

    def ass(self, way='equal'):
        try:
            assert_dict = {
                'equal': lambda: self._excp == self._resp,
                'in': lambda: self._excp in self._resp,
                'unequal': lambda: self._excp != self._resp
            }.get(way)
            return assert_dict()
        except Exception as err:
            logger.error(err)


if __name__ == '__main__':
    r = Assert(123, 13).ass('equal')
    print(r)