#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/4/21 10:24
# @Author : 谈林海
import os
import shutil


class CleanFile:
    """清理文件夹"""

    def __init__(self, path):
        self._path = path

    def __call__(self, *args, **kwargs):
        """
        如果文件夹不存在就创建，如果文件存在就清空
        """
        if not os.path.exists(self._path):
            os.mkdir(self._path)
        else:
            shutil.rmtree(self._path)
            os.mkdir(self._path)


if __name__ == '__main__':
    pass