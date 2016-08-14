#encoding=utf-8

from random import randint

start_list = range(1,10)

def random100(arr):
	res = list(arr)
	length = len(arr)
	for i in range(length):
		num = randint(1,length)
		tmp = res[i]
		res[i] = res[num-1]
		res[num-1] = tmp
	return res

#test random100	
for i in range(6):
	a=random100(start_list)
	print a

