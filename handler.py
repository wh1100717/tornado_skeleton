#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from util import TemplateUtil
from controller import UserController
from controller import DeviceController
from controller import GroupController
from controller import FriendController

defaultHandler = tornado.web.RequestHandler

class SpecificHandler(TemplateUtil.DefaultHandler):
    def get(self):
        self.write("This is the Specific Handler Page!")

class MainHandler(TemplateUtil.DefaultHandler):
    def get(self, filename):
        self.write(TemplateUtil.render_template(filename))

#####################User Handlers###############
class UserRegisterHandler(defaultHandler):
	def get(self):
		username = self.get_argument('username')
		password = self.get_argument('password')
		res = UserController.register(username,password)
		self.write("username: " + username + " | password: " + password + "<br>")
		self.write(str(res))

class UserLoginHandler(defaultHandler):
	def get(self):
		username = self.get_argument('username')
		password = self.get_argument('password')
		res = UserController.login(username, password)
		self.write(res)

class UserLogoutHandler(defaultHandler):
	def get(self):
		username = self.get_argument('username')
		res = UserController.logout(username)
		self.write(res)


# class UserUpdateInfoHandler(defaultHandler):
# 	def get(self):
# 		uid = self.get_argument('uid')
# 		nick_name = self.get_argument('nick_name')
# 		sex = self.get_argument('sex')

# class UserUpdateAvatarHandler(defaultHandler):
# 	def get(self):
# 		pass

# class UserUpdateEmailHandler(defaultHandler):
# 	def get(self):
# 		uid = self.get_argument('uid')
# 		email = self.get_argument('email')
# 		res = UserController.update_email(uid, email)
# 		self.write(res)

# class UserVerifyEmailHandler(defaultHandler):
# 	def get(self):
# 		verify_code = self.get_argument('verify_code')
# 		res = UserController.verify_email(verify_code)
# 		self.write(res)

# class UserUpdatePhoneNumberHandler(defaultHandler):
# 	def get(self):
# 		uid = self.get_argument('uid')
# 		phone_number = self.get_argument('phone_number')
# 		verify_code = self.get_argument('verify_code')
# 		res = UserController.update_phone_number(uid, phone_number, verify_code)
# 		self.write(res)

# class UserSendPhoneVerifyCodeHandler(defaultHandler):
# 	def get(self):
# 		phone_umber = self.get_argument('phone_umber')
# 		res = UserController.send_phone_verify_code(phone_umber)
# 		self.write(res)

#####################Device Handlers###############

class DeviceEnrollRequestHandler(defaultHandler):
	'''
	##发送设备登记请求
	1. 	服务器根据imei寻找对应的cid
		if 寻找到对应的cid
			需要判断cid所属的group下是否只有该设备
			if 只有该设备
				1. 	取消设备和组的关联关系
				2. 	取消该组和用户之间的关联关系
				3. 	删除该组
			else
				return 该设备已经属于别的组，需要取消从属关系才能登记
		else
			则说明该设备还没有登记过，执行step 2 登记流程
	2. 	登记流程
		获取cid
		根据cid push登记允许请求
	'''
	def get(self):
		imei = self.get_argument('imei')
		group_id = self.get_argument('group_id')
		device_type = self.get_argument('device_type')
		res = DeviceController.enroll(imei, group_id, device_type)
		self.write(res)

class DeviceEnrollAcceptHandler(defaultHandler):
	'''
	##发送设备登记允许请求
	1. 	判断accept
	'''
	def get(self):
		accept = self.get_argument('accept')
		pass

class DeviceUnenrollHandler(defaultHandler):
	def get(self):
		uid = self.get_argument('uid')
		cid = self.get_argument('cid')
		res = DeviceController.unenroll(uid, cid)
		self.write(res)

class DeviceListHandler(defaultHandler):
	def get(self):
		uid = self.get_argument('uid')
		res = DeviceController.list(uid)
		self.write(res)

# class DeviceSyncHandler(defaultHandler):
# 	def get(self):
# 		res = DeviceController.sync()
# 		self.write(res)

# #####################Group Handlers###################
# class GroupCreateHandler(defaultHandler):
# 	def get(self):
# 		uid = self.get_argument('uid')
# 		group_name = self.get_argument('group_name')
# 		group_type = self.get_argument('group_type')
# 		res = GroupController.create(uid, group_name, group_type)
# 		self.write(res)

# class GroupDeleteHandler(defaultHandler):
# 	def get(self):
# 		uid = self.get_argument('uid')
# 		gid = self.get_argument('gid')
# 		res = GroupController.delete(uid, gid)
# 		self.write(res)

# class GroupInviteMembersHandler(defaultHandler):
# 	def get(self):
# 		uid = self.get_argument('uid')
# 		gid = self.get_argument('gid')
# 		fid_list = self.get_argument('fid_list').split(',')
# 		res = GroupController.invite_members(uid, gid, fid_list)
# 		self.write(res)

# class GroupRemoveMembersHandler(defaultHandler):
# 	def get(self):
# 		uid = self.get_argument('uid')
# 		gid = self.get_argument('gid')
# 		fid_list = self.get_argument('fid_list').split(',')
# 		res = GroupController.delete_members(uid, gid, fid_list)
# 		self.write(res)

# class GroupSetAdminHandler(defaultHandler):
# 	def get(self):
# 		uid = self.get_argument('uid')
# 		gid = self.get_argument('gid')
# 		fid = self.get_argument('fid')
# 		res = GroupController.set_admin(uid, gid, fid)
# 		self.write(res)

# class GroupRemoveAdminHandler(defaultHandler):
# 	def get(self):
# 		uid = self.get_argument('uid')
# 		gid = self.get_argument('gid')
# 		fid = self.get_argument('fid')
# 		res = GroupController.remove_admin(uid, gid, fid)
# 		self.write(res)

# class GroupMemberListHandler(defaultHandler):
# 	def get(self):
# 		uid = self.get_argument('uid')
# 		gid = self.get_argument('gid')
# 		res = GroupController.member_list(uid, gid)
# 		self.write(res)

# class GroupMessageBroadcastHandler(defaultHandler):
# 	def get(self):
# 		uid = self.get_argument('uid')
# 		gid = self.get_argument('gid')
# 		msg_type = self.get_argument('msg_type')
# 		msg_content = self.get_argument('msg_content')
# 		res = GroupController.message_broadcast(uid, gid, msg_type, msg_content)
# 		self.write(res)

# #####################Friend Handlers###################
# class FriendAddHandler(defaultHandler):
# 	def get(self):
# 		uid = self.get_argument('uid')
# 		fid = self.get_argument('fid')
# 		res = FriendController.add(uid, fid)
# 		self.write(res)

# class FriendAcceptHandler(defaultHandler):
# 	def get(self):
# 		uid = self.get_argument('uid')
# 		fid = self.get_argument('fid')
# 		res = FriendController.accept(uid, fid)
# 		self.write(res)

# class FriendRemoveHandler(defaultHandler):
# 	def get(self):
# 		uid = self.get_argument('uid')
# 		fid = self.get_argument('fid')
# 		res = FriendController.remove(uid, fid)
# 		self.write(res)





handlers = [
	#User Handlers
	(r"/user/register", UserRegisterHandler), #用户注册
	(r"/user/login", UserLoginHandler),	#用户登录
	(r"/user/logout", UserLogoutHandler), #用户登出
	#Device Handlers
	(r"/device/enroll/request", DeviceEnrollRequestHandler), #设备登记
	(r"/device/unenroll", DeviceUnenrollHandler), #设备注销
	(r"/device/list", DeviceListHandler), #获取登记设备列表
	# #Group Handlers
	# (r"/group/create",GroupCreateHandler),
	# #Friend Handlers

	#Request Sample
    (r"/specific_request", SpecificHandler),
    (r"^(.*)$", MainHandler),
]




