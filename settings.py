#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

#根目录
__root_dir__ = os.path.dirname(__file__)
#模板目录
__template_dir__ = os.path.join(__root_dir__, "templates")
#静态文件目录
__static_dir__ =  os.path.join(__root_dir__, "static")
#黑名单列表
__blacklist_templates__ = ('layouts',)

#服务器端口
server_port = 80

#服务器配置
server_config = {
    "static_path": __static_dir__,
    "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
    "login_url": "/login",
    "xsrf_cookies": True,
    "debug": True,
}