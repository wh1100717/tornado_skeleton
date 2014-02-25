#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo
import settings

mongo_config = settings.mongo_config

class MongoClient(object):
	def __init__(self):
		self.mongo_client = pymongo.MongoClient(mongo_config['host'], mongo_config['port'])

	def get_db(self, db_name = mongo_config['db_name']):
		'''
		##获取数据库
		'''
		return self.mongo_client[db_name]

