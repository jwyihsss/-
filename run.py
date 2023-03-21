#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pytest
import click


@click.command()
@click.option('--mark', '-m', default='', help='传入被标记的case套件, 例: -m login')
def run(mark):
    pytest.main(['test_cases', f'-m={mark}', '--clean-alluredir', '--alluredir=allure-results'])
    os.system("allure generate -c -o allure-report")


if __name__ == '__main__':
    print("""                 
       开始执行项目...
       """)
    run()
