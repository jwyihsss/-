#!/usr/bin/env prespthon
# -*- coding: utf-8 -*-
# @Time : 2023/4/24 15:59
# @Author : 谈林海
from utils.singleton_control import SingletonPattern


@SingletonPattern
class Assert:
    """断言类"""

    def __init__(self, error_msg='assert error'):
        self.error_msg = error_msg

    def asserts(self, way='equal'):
        assert_dict = {
            'equal': lambda excp, resp: self.equal(excp, resp),
            'unequal': lambda excp, resp: self.not_equal(excp, resp),
            'in': lambda excp, resp: self.is_in(excp, resp),
            'not_in': lambda excp, resp: self.is_not_in(excp, resp),
            'true': lambda assertion: self.is_true(assertion),
            'false': lambda assertion: self.is_false(assertion),
            'none': lambda excp: self.is_none(excp),
            'not_none': lambda excp: self.is_not_none(excp)
        }.get(way)
        return assert_dict

    def is_true(self, assertion):
        """断言为真"""

        return self._handle_error() if not assertion else True

    def is_false(self, assertion):
        """断言为假"""

        return self._handle_error() if assertion else True

    def equal(self, excp, resp):
        """断言相等"""

        return self._handle_error() if excp != resp else True

    def not_equal(self, excp, resp):
        """断言不相等"""

        return self._handle_error() if excp == resp else True

    def is_in(self, excp, resp):
        """断言包含"""

        return self._handle_error() if excp not in resp else True

    def is_not_in(self, excp, resp):
        """断言不包含"""

        return self._handle_error() if excp in resp else True

    def is_none(self, excp):
        """断言为None"""

        return self._handle_error() if excp is not None else True

    def is_not_none(self, excp):
        """断言不为None"""

        return self._handle_error() if excp is None else True

    def _handle_error(self):
        """处理断言错误"""

        if self.error_msg:
            raise AssertionError(self.error_msg)
        else:
            raise AssertionError()


if __name__ == '__main__':
    r = Assert().asserts('equal')(1, 1)
    print(r)