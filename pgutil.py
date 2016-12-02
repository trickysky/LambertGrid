#!/usr/bin/python
# -*- coding=UTF-8 -*-
# trickysky
# 2016/12/1

import psycopg2 as pg

class Database(object):
	def __init__(self, dbName, user='postgres', pwd='tk0306', host='localhost', port=5432):
		self.dbName = dbName
		self.host = host
		self.user = user
		self.password = pwd
		self.port = port
		self.conn = self.get_connection(dbName)

	def __del__(self):
		try:
			self.conn.close()
		except:
			pass
		self.conn = None

	def execute(self, sql):
		try:
			conn = self.get_connection(self.dbName)
			cur = conn.cursor()
			cur.execute(sql)
			conn.commit()
			conn.close()
			return True
		except:
			print 'error sql:%s' % sql
			try:
				conn = self.get_connection(self.dbName)
				conn.rollback()
				conn.close()
			except:
				conn = self.get_connection(self.dbName)
				conn.close()
			return False

	def get_resultSet(self, queryStr):
		try:
			conn = self.get_connection(self.dbName)
			cur = conn.cursor()
			cur.execute(queryStr)
			rows = cur.fetchall()
			cur.close()
			conn.close()
			return rows
		except:
			try:
				conn.rollback()
			except:
				print 'SQL error:%s' % queryStr
				self.conn = self.get_connection(self.dbName)
				self.conn.rollback()
			return None

	def get_connection(self, dbName):
		return pg.connect(host=self.host, port=self.port, user=self.user, password=self.password, database=dbName)