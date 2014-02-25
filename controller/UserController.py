#!/usr/bin/env python
# -*- coding: utf-8 -*-

from util import MongoUtil

mongo_client = MongoUtil.MongoClient()
db = mongo_client.get_db()
user_collection = db.users

def register(username, password):
	'''
	##`用户注册`请求
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
	*	paras:
		*	username: 用户登录名
		*	password: 密码
	*	response:
		*	status:
			success: 注册成功
			username_exist: 表示用户名已存在
			fail: 其他错误(暂时不细分)
		*	uid: 该用户的唯一标识
	'''
	count = user_collection.find({'username':username}).count()
	print count
	if count > 0:
		return {'status':'username_exist'}
	else:
		#TODO 需要对password进行md5加密
		user = {'username':username, 'password':password}
		user_collection.insert(user)
	return {'status':'success', 'username':username}

def login(username, password):
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
	*	paras:
		*	username: 用户登录名
		*	password: 密码
	*	response:
		*	status:
			success: 表示登陆成功
			username_not_exist: 表示该用户名不存在
			password_incorrect: 表示密码错误
			fail: 表示其他错误(暂时不细分)
		*	uid: 用户唯一标识
	'''

	# 检查username在数据库中是否存在，如果不存在则返回`username_not_exist`
	# 核对password是否正确，如果不正确，则返回`password_incorrect`
	# 查询并返回uid
	user = user_collection.find_one({'username':username})
	if not user:
		return {'status':'username_not_exist'}
	if user['password'] == password:
		return {'status':'success', 'uid':uid}
	else:
		return {'status':'password_incorrect'}

def logout():
	'''
	##`用户登出`请求
	1. 	获取uid并进行相应的session操作
	'''
	return 





