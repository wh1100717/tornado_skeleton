#!/usr/bin/env python
# -*- coding: utf-8 -*-

def register(username, password):
	'''
	##用户注册流程(暂定) --> 账户和设备分离，注册流程主要针对的是账户注册，账户和设备是一对多的关系。
	*	paras:
		*	username: 用户登录名
		*	password: 密码
	*	response:
		*	status: `success`表示注册成功 | `username_exist`表示用户名已存在 | `fail`表示其他错误(暂时不细分)
		*	uid: 该用户的唯一标识
	'''

	#TODO 检查username在数据库中是否存在, 如果存在则返回`username_exist`
	#TODO 往数据库中插入数据
	uid = 123
	return {'status':'success', 'uid':uid}

def login(username, password):
	'''
	##用户登陆流程(暂定) --> 用户登陆只负责具体的登陆流程， 设备信息同步等流程放在登陆成功后进行处理
	*	paras:
		*	username: 用户登录名
		*	password: 密码
	*	response:
		*	status: `success`表示登陆成功 | `username_not_exist`表示该用户名不存在 | `password_incorrect`表示密码错误 | `fail`表示其他错误(暂时不细分)
		*	uid: 用户唯一标识
	'''

	#TODO 检查username在数据库中是否存在，如果不存在则返回`username_not_exist`
	#TODO 核对password是否正确，如果不正确，则返回`password_incorrect`
	#查询并返回uid
	uid = 123
	return {'status':'success', 'uid':uid}