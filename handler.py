#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from util import TemplateUtil
from controller import UserController
from controller import DeviceController
from controller import GroupController
from controller import FriendController

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
    	user = self.get_secure_cookie("user")
    	print user
    	return user


#####################User Handlers###############
class UserRegisterHandler(BaseHandler):
	'''
	##`用户注册`请求
	#***更改为手机号注册
	1. 	检查username格式是否合规
		if 不合规
			则说明username存在一些问题，包括是否有sql注入等行为  return
		else
			执行step 2
	2. 	判断username是否已经存在
		if 存在
			则说明该用户名已经注册，需要更换一个新的用户名 return
		else
			执行step 3
	3. 	利用md5对password求哈希散列
	4. 	插入data_store
	'''
	def get(self):
		username = self.get_argument('username')
		password = self.get_argument('password')
		res = UserController.register(username,password)
		self.write("username: " + username + " | password: " + password + "<br>")
		self.write(str(res))


##**** 增加验证码的判断


class UserLoginHandler(BaseHandler):
	'''
	##`用户登录`请求
	1. 	检查username格式是否合规
		if 不合规
			则说明username存在一些问题，包括是否有sql注入等行为  return
		else
			执行step 2
	2. 	利用md5对password求哈希散列
	3. 	将加密后的password和存储在数据库中username对应的password进行比对
		if 相同
			则说明登录成功，进行session等操作 return uid
		else
			则说明密码错误，return password error
	'''
	def get(self):
		username = self.get_argument('username')
		password = self.get_argument('password')
		res = UserController.login(username, password)
		if res['status'] == 'success':
			self.set_secure_cookie("user", username)
			self.redirect("/")
		else:
			self.write(res)


class UserLogoutHandler(BaseHandler):
	'''
	##`用户登出`请求
	1. 	获取uid并进行相应的session操作
	'''
	def get(self):
		self.clear_cookie("user")
		self.write("logout successfullly")



# class UserUpdateInfoHandler(BaseHandler):
# 	def get(self):
# 		uid = self.get_argument('uid')
# 		nick_name = self.get_argument('nick_name')
# 		sex = self.get_argument('sex')

# class UserUpdateAvatarHandler(BaseHandler):
# 	def get(self):
# 		pass

# class UserUpdateEmailHandler(BaseHandler):
# 	def get(self):
# 		uid = self.get_argument('uid')
# 		email = self.get_argument('email')
# 		res = UserController.update_email(uid, email)
# 		self.write(res)

# class UserVerifyEmailHandler(BaseHandler):
# 	def get(self):
# 		verify_code = self.get_argument('verify_code')
# 		res = UserController.verify_email(verify_code)
# 		self.write(res)

# class UserUpdatePhoneNumberHandler(BaseHandler):
# 	def get(self):
# 		uid = self.get_argument('uid')
# 		phone_number = self.get_argument('phone_number')
# 		verify_code = self.get_argument('verify_code')
# 		res = UserController.update_phone_number(uid, phone_number, verify_code)
# 		self.write(res)

# class UserSendPhoneVerifyCodeHandler(BaseHandler):
# 	def get(self):
# 		phone_umber = self.get_argument('phone_umber')
# 		res = UserController.send_phone_verify_code(phone_umber)
# 		self.write(res)

#####################Device Handlers###############

class DeviceEnrollRequestHandler(BaseHandler):
	'''
	##`请求设备登记`请求
	1.	获取要登记的设备imei、cid、device_type信息，同时获取用户所拥有的group_id
	2. 	利用push平台发送请求给对应cid的设备，等待设备确认信息
	'''
	def get(self):
		imei = self.get_argument('imei')
		cid = self.get_argument('cid')
		group_id = self.get_argument('group_id')
		device_type = self.get_argument('device_type')
		res = DeviceController.enroll(imei, cid, group_id, device_type)
		self.write(res)

class DeviceEnrollAcceptHandler(BaseHandler):
	'''
	##`允许设备登记`请求
	1. 	判断accept
		if false
			则说明用户拒绝登记设备，做一些清理工作，return该设备拒绝接受设备登记申请
	2. 	服务器根据imei寻找对应的cid
		if 寻找imei对应的cid
			比对系统记录cid和传入cid是否相同
			if 不同
				则说明可能由于手机被刷机等原因软件被直接卸载，没有执行清理工作，需要进行更换cid等逻辑
			需要判断cid所属的group下是否只有该设备
			if 只有该设备
				1. 	取消设备和组的关联关系
				2. 	取消该组和用户之间的关联关系
				3. 	删除该组
				4. 	执行step 2 登记流程
			else
				return 该设备已经属于别的组，需要取消从属关系才能登记
		else
			则说明该设备还没有登记过，执行step 2 登记流程
	2. 	登记流程
		设备和组做关联
	'''
	def get(self):
		accept = self.get_argument('accept')
		imei = self.get_argument('imei')
		cid = self.get_argument('cid')
		group_id = self.get_argument('group_id')
		device_type = self.get_argument('device_type')
		pass

class DeviceUnenrollHandler(BaseHandler):
	'''
	##`设备注销`请求
	1. 	根据cid获取其所属的group_id
		if 没有查询到group_id
			说明cid不属于任何的组，也就不需要注销了，return
		else
			执行step 2
	2. 	查询uid是否拥有该group_id
		if 没有group_id
			说明uid没有管理该group中设备的权限，不能注销该组设备，return
		else
			执行step 3
	3. 	注销流程
		取消group_id和cid之间的关系
	'''
	def get(self):
		uid = self.get_argument('uid')
		cid = self.get_argument('cid')
		res = DeviceController.unenroll(uid, cid)
		self.write(res)

class DeviceListHandler(BaseHandler):
	'''
	##`获取设备列表`请求
	1. 	判断用户是否拥有查看该group的权限，如果没有，return 错误
	2. 	push请求查看在线设备，并进行数据封装
	'''
	def get(self):
		group_id = self.get_argument('group_id')
		uid = self.get_argument('uid')
		res = DeviceController.list(uid, group_id)
		self.write(res)

# class DeviceSyncHandler(BaseHandler):
# 	def get(self):
# 		res = DeviceController.sync()
# 		self.write(res)

# #####################Group Handlers###################
# class GroupCreateHandler(BaseHandler):
# 	def get(self):
# 		uid = self.get_argument('uid')
# 		group_name = self.get_argument('group_name')
# 		group_type = self.get_argument('group_type')
# 		res = GroupController.create(uid, group_name, group_type)
# 		self.write(res)

# class GroupDeleteHandler(BaseHandler):
# 	def get(self):
# 		uid = self.get_argument('uid')
# 		gid = self.get_argument('gid')
# 		res = GroupController.delete(uid, gid)
# 		self.write(res)

# class GroupInviteMembersHandler(BaseHandler):
# 	def get(self):
# 		uid = self.get_argument('uid')
# 		gid = self.get_argument('gid')
# 		fid_list = self.get_argument('fid_list').split(',')
# 		res = GroupController.invite_members(uid, gid, fid_list)
# 		self.write(res)

# class GroupRemoveMembersHandler(BaseHandler):
# 	def get(self):
# 		uid = self.get_argument('uid')
# 		gid = self.get_argument('gid')
# 		fid_list = self.get_argument('fid_list').split(',')
# 		res = GroupController.delete_members(uid, gid, fid_list)
# 		self.write(res)

# class GroupSetAdminHandler(BaseHandler):
# 	def get(self):
# 		uid = self.get_argument('uid')
# 		gid = self.get_argument('gid')
# 		fid = self.get_argument('fid')
# 		res = GroupController.set_admin(uid, gid, fid)
# 		self.write(res)

# class GroupRemoveAdminHandler(BaseHandler):
# 	def get(self):
# 		uid = self.get_argument('uid')
# 		gid = self.get_argument('gid')
# 		fid = self.get_argument('fid')
# 		res = GroupController.remove_admin(uid, gid, fid)
# 		self.write(res)

# class GroupMemberListHandler(BaseHandler):
# 	def get(self):
# 		uid = self.get_argument('uid')
# 		gid = self.get_argument('gid')
# 		res = GroupController.member_list(uid, gid)
# 		self.write(res)

# class GroupMessageBroadcastHandler(BaseHandler):
# 	def get(self):
# 		uid = self.get_argument('uid')
# 		gid = self.get_argument('gid')
# 		msg_type = self.get_argument('msg_type')
# 		msg_content = self.get_argument('msg_content')
# 		res = GroupController.message_broadcast(uid, gid, msg_type, msg_content)
# 		self.write(res)

# #####################Friend Handlers###################
# class FriendAddHandler(BaseHandler):
# 	def get(self):
# 		uid = self.get_argument('uid')
# 		fid = self.get_argument('fid')
# 		res = FriendController.add(uid, fid)
# 		self.write(res)

# class FriendAcceptHandler(BaseHandler):
# 	def get(self):
# 		uid = self.get_argument('uid')
# 		fid = self.get_argument('fid')
# 		res = FriendController.accept(uid, fid)
# 		self.write(res)

# class FriendRemoveHandler(BaseHandler):
# 	def get(self):
# 		uid = self.get_argument('uid')
# 		fid = self.get_argument('fid')
# 		res = FriendController.remove(uid, fid)
# 		self.write(res)


class SpecificHandler(BaseHandler):
    def get(self):
        self.write("This is the Specific Handler Page!")

class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.write("123")

handlers = [
	#User Handlers
	(r"/user/register", UserRegisterHandler), #用户注册
	(r"/user/login", UserLoginHandler),	#用户登录
	(r"/user/logout", UserLogoutHandler), #用户登出
	#Device Handlers
	(r"/device/enroll/request", DeviceEnrollRequestHandler), #设备登记
	(r"/device/unenroll", DeviceUnenrollHandler), #设备注销
	(r"/device/list", DeviceListHandler), #获取登记设备列表

	#Request Sample
    (r"/specific_request", SpecificHandler),
    (r"^.*$", MainHandler),
]




