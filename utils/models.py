#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Union
from pydantic import BaseModel


class Jenkins(BaseModel):
    url: Union[str, None]
    mapping_url: Union[str, None]
    user: Union[str, int, None]
    pwd: Union[str, int, None]
    project: Union[str, None]


class DingTalk(BaseModel):
    webhook: Union[str, None]


class MySqlDB(BaseModel):
    host: Union[str, None]
    user: Union[str, None]
    password: Union[str, None]
    port: Union[int, None]


class Config(BaseModel):
    project_name: Union[str, None]
    env: Union[str, None]
    tester_name: Union[str, None]
    host: Union[str, None]
    account: Union[str, int, None]
    password: Union[str, int, None]
    jenkins: "Jenkins"
    ding_talk: "DingTalk"
    mysql_db: "MySqlDB"


