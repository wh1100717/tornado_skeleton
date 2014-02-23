#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from util import TemplateUtil
from controller import UserController
from controller import DeviceController

class SpecificHandler(TemplateUtil.DefaultHandler):
    def get(self):
        self.write("This is the Specific Handler Page!")

class MainHandler(TemplateUtil.DefaultHandler):
    def get(self, filename):
        self.write(TemplateUtil.render_template(filename))

#####################User Hanlders###############

class UserRegisterHandler(tornado.web.RequestHandler):
	def get(self):
		username = self.get_argument('username')
		password = self.get_argument('password')
		res = UserController.register(username,password)
		self.write("username: " + username + " | password: " + password + "<br>")
		self.write(str(res))

class UserLoginHandler(tornado.web.RequestHandler):
	def get(self):
		username = self.get_argument('username')
		password = self.get_argument('password')
		res = UserController.login(username, password)
		self.write(res)

#####################Device Hanlders###############

class DeviceEnrollHandler(tornado.web.RequestHandler):
	def get(self):
		uid = self.get_argument('uid')
		imei = self.get_argument('imei')
		phone_type = self.get_argument('phone_type')
		res = DeviceController.enroll(uid, imei, phone_type)
		self.write(res)

class DeviceUnenrollHandler(tornado.web.RequestHandler):
	def get(self):
		uid = self.get_argument('uid')
		cid = self.get_argument('cid')
		res = DeviceController.unenroll(uid, cid)
		self.write(res)

class DeviceSyncHandler(tornado.web.RequestHandler):
	def get(self):
		res = DeviceController.sync()
		self.write(res)

class DeviceListHandler(tornado.web.RequestHandler):
	def get(self):
		uid = self.get_argument('uid')
		res = DeviceController.list(uid)
		self.write(res)

#####################Group Hanlders###################


handlers = [
	#User Handlers
	(r"/user/register", UserRegisterHandler), #用户注册
	(r"/user/login", UserLoginHandler),	#用户登录
	#Device Handlers
	(r"/device/enroll", DeviceEnrollHandler), #设备登记
	(r"/device/unenroll", DeviceUnenrollHandler), #设备注销
	(r"/device/sync", DeviceSyncHandler), #设备同步
	(r"/device/list", DeviceListHandler), #获取登记设备列表
	#Group Handlers

	#Request Sample
    (r"/specific_request", SpecificHandler),
    (r"^(.*)$", MainHandler),
]




