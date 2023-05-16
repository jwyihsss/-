#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import enum
import pymysql
from utils import config
from utils import logger
from utils.commons.singleton_control import SingletonPattern


class QueryState(enum.Enum):
    ALL = "all"
    ONE = "one"


@SingletonPattern
class MysqlDB:
    """数据库封装"""

    def __init__(self):
        """初始化数据库连接"""

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

    def __del__(self):
        """关闭数据库连接"""

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
                data = cursor.fetchall() if state == QueryState.ALL else cursor.fetchone() if state == QueryState.ONE else ...
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
