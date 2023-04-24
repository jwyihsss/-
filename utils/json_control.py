#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/4/10 10:56
# @Author : 谈林海
from jsonpath import jsonpath
from utils.log_control import logger


def get_json(res, key):
    try:
        val = jsonpath(res, f'$..{key}')
        return val[0] if len(val) == 1 else val
    except Exception as err:
        logger.error(f'json提取值失败，请检查: {err}')
        raise


if __name__ == '__main__':
    pass