#!/usr/bin/env python
# -*- coding: utf-8 -*-

def enroll(uid, imei, phone_type):
	'''
	##设备登记流程(暂定)  --> 当用户利用该设备登陆后，需要对该设备进行登记，实现用户管理自己多台设备的能力
	*	paras:
		*	uid: 用户的唯一标识
		*	imei: 移动设备唯一标识
		*	phone_type: 设备类型，默认为`android`
				android: 安卓系统
				ios: 苹果系统
		*	(设备的基础信息等)+
	*	repsonse:
		*	status: 返回状态标识符
				success: 表示登记成功
				identify_fail: 表示用户合法性认证失败
				device_exist: 表示该台设备已经登记
				fail: 表示其他错误(暂时不细分)
		*	cid: 服务器端生成的`client_id`，用来作为推送时客户端的唯一标识
	'''

	#TODO 对请求合法性做验证，如果失败返回`identify_fail`
	#TODO 检查设备是否存在，如果存在则返回`device_exist`
	#TODO 生成cid作为设备的唯一标识，并返回
	cid = 1111111
	return {'status':'success', 'cid':cid}

def unenroll(uid, cid):
	'''
	##注销设备流程(暂定) --> 用户可以进行注销当前设备或者利用主控端来注销设备其他设备
	*	paras:
		*	uid: 用户的唯一标识
		*	cid: 客户端唯一标识
	*	response:
		*	status: 返回状态标识符
				success: 表示设备注销成功
				identify_fail: 表示用户合法性认证失败
				authorize_fail: 表示用户没有注销该设备的权限
				fail: 表示其他错误(暂时不细分)
	'''
	#TODO 对请求进行合法性校验，如果失败则返回`identify_fail`
	#TODO 对uid进行是否有删除cid权限校验，如果失败则返回`authorize_fail`，表示该用户没有注销该设备的权限
	#TODO 注销流程
	return {'status':'success'}

def list(uid):
	'''
	##获取当前用户登记设备列表(暂定) --> 用户可以查看当前等级的设备列表
	*	paras:
		*	uid: 用户的唯一标识
	*	response:
		*	status: 返回状态标识符
				success: 获取等级设备列表成功
				identify_fail: 表示用户合法性认证失败
				fail: 表示其他错误(暂时不细分)
		*	device_list: 设备信息列表
	'''
	#TODO 对请求进行合法性校验，如果失败则返回`identify_fail`
	device_list = [{'cid':1,'online':True},{'cid':2,'online':False}]
	return {'status':'success', 'device_list':device_list}

def sync():
	'''
	##用户设备enroll以后，需要进行数据同步
	'''
	pass





