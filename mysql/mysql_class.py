#encoding=utf-8

import re
import time
import MySQLdb

class Mysql(object):
	"""Mysql python class to manipulate MySQL."""
	_dbconfig = None
	_cursor = None
	_connect = None
	_error_code = '' # error_code from MySQLdb

	TIMEOUT_DEADLINE = 30 # quit if TIMEOUT_TOTAL over TIMEOUT_DEADLINE
	TIMEOUT_TOTAL = 0 # total time the connects have cost
	TIMEOUT_THREAD = 10 # timeout of one connect


	def __init__(self, dbconfig):
		self._dbconfig = dbconfig
		self.dbconfig_test(dbconfig)
		try:
			self._connect = MySQLdb.connect(
				host = self._dbconfig['host'],
				port = self._dbconfig['port'],
				user = self._dbconfig['user'],
				passwd = self._dbconfig['passwd'],
				db = self._dbconfig['db'],
				charset = self._dbconfig['charset'],
				connect_timeout = self.TIMEOUT_THREAD)
		except MySQLdb.Error, e:
			self._error_code = e.args[0]

			errorMsg = "%s: %s, %s" % (type(e).__name__, e.args[0], e.args)
			# reconnect if not reach TIMEOUT_DEADLINE.
			if self.TIMEOUT_TOTAL < self.TIMEOUT_DEADLINE:
				interval = 1
				self.TIMEOUT_TOTAL ++ (interval + self.TIMEOUT_THREAD)
				time.sleep(interval)
				return self.__init__(dbconfig)
			raise Exception(errorMsg)

		if self._dbconfig.has_key('cursorType') and self._dbconfig['cursorType'] == 'list':
			self._cursor = self._connect.cursor()
		else:
			self._cursor = self._connect.cursor(MySQLdb.cursors.DictCursor)
		self._cursor.execute("set names utf8")

	def dbconfig_test(self, dbconfig):
		if type(dbconfig) is not dict:
			raise ValueError('dbconfig is not dict')
		else:
			for key in ['host','port','user','passwd','db']:
				if not dbconfig.has_key(key):
					raise ValueError('dbconfig missing %s' % key)
			if not dbconfig.has_key('charset'):
				self._dbconfig['charset'] = 'utf8'

	def select(self, sql, ret_type='all', ret_format='array'):
		'''select or show'''
		self._cursor.execute(sql)
		if ret_type == 'all':
			if (self._dbconfig.has_key('cursorType') and self._dbconfig['cursorType'] == 'list') or ret_format == 'row':
				return self._cursor.fetchall()
			else:
				return self.rows2array(self._cursor.fetchall())
		elif ret_type == 'one':
			return self._cursor.fetchone()
		elif ret_type == 'count':
			return self._cursor.rowcount


	def dml(self, sql):
		'''update or delete or insert'''
		self._cursor.execute(sql)
		self._cursor.commit()
		type = self.dml_type(sql) 
		# if primary key is auto increase, return inserted ID.
		if type == 'insert':
			return self._connect.insert_id()
		else:
			return True

	def query(self, sql):
		'''general query'''
		self._cursor.execute(sql)
		self._connect.commit()
		return True

	def dml_type(self, sql):
		re_dml = re.compile('^(?P<dml>\w+)\s+', re.I)
		m = re_dml.match(sql)
		if m:
			if m.group('dml').lower() == 'delete':
				return 'delete'
			elif m.group('dml').lower() == 'update':
				return 'update'
			elif m.group('dml').lower() == 'insert':
				return 'insert'
		raise ValueError('%s is not dml.' % sql)

	def rows2array(self, data):
		'''transfer tuple to arrry'''
		result = []
		for da in data:
			if type(da) is not dict:
				raise ValueError('return data is not a dict.')
			result.append(da)
		return result

	def __del__(slef):
		'''free source'''
		self._cursor.close()
		self._connect.close()

	def close(self):
		self.__del__()
