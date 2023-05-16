#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/4/7 14:00
# @Author : 谈林海
import http.cookiejar as cj
from datetime import datetime, timedelta

from utils import config
from utils.commons.get_md5_control import Md5


def create_cookie():
    """生成cookie"""

    cookie_jar = cj.CookieJar()
    cookie = cj.Cookie(
        version=0,
        name='cookies',
        value=Md5.getmd5(config.host),
        port=None,
        port_specified=False,
        domain=config.host,
        domain_specified=True,
        domain_initial_dot=False,
        path='/',
        path_specified=True,
        secure=True,
        expires=int((datetime.now() + timedelta(days=30)).timestamp()),
        discard=False,
        comment=None,
        comment_url=None,
        rest={}
    )
    cookie_jar.set_cookie(cookie)
    return cookie_jar


Cookies = create_cookie()