#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Union
from pydantic import BaseModel, validator
from typing import Text


class Jenkins(BaseModel):
    """Jenkins配置"""

    url: Union[str, None]
    mapping_url: Union[str, None]
    user: Union[str, int, None]
    pwd: Union[str, int, None]
    project: Union[str, None]


class DingTalk(BaseModel):
    """钉钉消息推送"""

    webhook: Union[str, None]
    test_webhook: Union[str, None]


class MySqlDB(BaseModel):
    """数据库配置"""

    host: Union[str, None]
    user: Union[str, None]
    password: Union[str, None]
    port: Union[int, None]
    switch: Union[bool, None] = False


class Email(BaseModel):
    """邮箱配置"""

    smtp_server: Union[Text, None]
    sender_email: Union[Text, None]
    password: Union[Text, None]
    receiver_email: Union[Text, None]


class Config(BaseModel):
    """全局配置"""

    project_name: Union[str, None]
    env: Union[str, None]
    tester_name: Union[str, None]
    host: Union[str, None]
    account: Union[str, int, None]
    password: Union[str, int, None]
    jenkins: "Jenkins"
    ding_talk: "DingTalk"
    mysql_db: "MySqlDB"
    email: "Email"

    @validator('host')
    def name_not_empty(cls, v):
        if isinstance(v, str) and len(v.strip()) == 0:
            raise ValueError("测试域名不能为空")
        return v


