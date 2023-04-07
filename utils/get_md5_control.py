#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/3/24 13:08
# @Author : 谈林海
import hashlib


class Md5:
    """md5加密"""

    @staticmethod
    def getmd5(key=None):
        """返回 key 的 md5 哈希值"""

        return hashlib.md5(key.encode('utf-8')).hexdigest()

    @staticmethod
    def getfilemd5(file_path):
        """返回文件 file_path 的 md5 哈希值"""

        with open(file_path, 'rb') as f:
            file_md5 = hashlib.md5(f.read()).hexdigest()
        return file_md5
