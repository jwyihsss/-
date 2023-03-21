#!/usr/bin/env python
# -*- coding: utf-8 -*-
from utils.path import root


def open_file(file):
    """封装接口请求打开文件 函数"""

    file_path = str(root / f'files/{file}')
    file_name = file_path.split('/')[-1]
    return {'file': (file_name, open(file_path, 'rb'), 'application/json')}


if __name__ == '__main__':
    r = open_file('avatar_new.png')
    print(r)