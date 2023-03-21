#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pymysql
from utils import config
from loguru import logger


class MysqlDB:
    """ 数据库 封装 """

    def __init__(self):
        try:
            # 建立数据库连接
            self.conn = pymysql.connect(
                host=config.mysql_db.host,
                user=config.mysql_db.user,
                password=config.mysql_db.password,
                port=config.mysql_db.port
            )
            self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        except Exception as err:
            logger.error(f"数据库连接失败, {err}")

    def __del__(self):
        try:
            self.cur.close()
            self.conn.close()
        except Exception as err:
            logger.error(f'数据库关闭连接失败, {err}')

    def query(self, sql, state="all"):
        """ 查询 """
        try:
            self.cur.execute(sql)

            if state == "all":
                # 查询全部
                data = self.cur.fetchall()
            else:
                # 查询单条
                data = self.cur.fetchone()
            return data
        except Exception as err:
            logger.error(f"数据库连接失败, {err}")
            raise

    def execute(self, sql):
        """ 更新、删除、新增 """
        try:
            rows = self.cur.execute(sql)
            self.conn.commit()
            return rows
        except Exception as err:
            logger.error(f"数据库连接失败, {err}")
            self.conn.rollback()
            raise


if __name__ == '__main__':
    pass