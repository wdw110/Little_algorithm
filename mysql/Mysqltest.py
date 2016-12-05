#encoding=utf-8

"""
author: wdw110
"""

from MySqlConn import Mysql 
from _sqlite3 import Row

#申请资源
mysql = Mysql()

sqlAll = ''
result = mysql.getAll(sqlAll)
if result:
	print 'get all'
	for row in result:
		print '%s\t%s'%()

sqlAll = ''
result = mysql.getMany(sqlAll,2)
if result:
	print 'get many'
	for row in result:
		print ''

result = mysql.getOne(sqlAll)
print 'get one'
print ''

#释放资源
mysql.dispose()