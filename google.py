#encoding=utf-8

#给定能随机生成整数 1 到 5 的函数，写出能随机生成整数 1 到 7 的函数。

import random

f = random.randint #给定能随机生成整数 1 到 5 的函数

def rand(n):   #随机生成整数 1 到 n 的函数
	tmp = [f(1,5) for i in range(n)]
	


