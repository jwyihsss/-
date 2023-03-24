#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import enum
import pymysql
from utils import config
from loguru import logger


class QueryState(enum.Enum):
    ALL = "all"
    ONE = "one"


class MysqlDB:
    """数据库封装"""

    def __enter__(self):
        try:
            self.conn = pymysql.connect(
                host=config.mysql_db.host,
                user=config.mysql_db.user,
                password=config.mysql_db.password,
                port=config.mysql_db.port,
                cursorclass=pymysql.cursors.DictCursor
            )
        except Exception as err:
            logger.error(f"数据库连接失败: {err}")
            raise
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.conn.close()
        except Exception as err:
            logger.error(f"数据库关闭连接失败: {err}")
            raise

    def query(self, sql, state=QueryState.ALL):
        """查询"""

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
                if state == QueryState.ALL:
                    data = cursor.fetchall()
                elif state == QueryState.ONE:
                    data = cursor.fetchone()
                else:
                    raise ValueError(f"无效的查询状态: {state}")
            return data
        except Exception as err:
            logger.error(f"查询失败: {err}")
            raise

    def execute(self, sql):
        """更新、删除、新增"""

        try:
            with self.conn.cursor() as cursor:
                rows = cursor.execute(sql)
            self.conn.commit()
            return rows
        except Exception as err:
            logger.error(f"执行失败: {err}")
            self.conn.rollback()
            raise
