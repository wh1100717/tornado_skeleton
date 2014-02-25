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
	"cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=", 
	"login_url": "/login",
	"xsrf_cookies": True,
	"debug": True,
}

#个推Push平台配置
igetui_config = {
	'APPKEY' : "请输入您的appkey",
	'APPID' : "请输入您的appid",
	'MASTERSECRET' : "请输入您的MASTERSECRET",
	'CID' : "测试客户端的CID",
	'HOST' : "http://sdk.open.api.igexin.com/apiex.htm",
	'CALLBACK_URL' : "",
}

#MongoDB配置
mongo_config = {
	'host' : "localhost",
	'port' : 27017,
	'db_name' : "tongtang"
}