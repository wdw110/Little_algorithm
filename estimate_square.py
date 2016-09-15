#encoding=utf-8

#判断一个自然数是否是某个数的平方。当然不能使用开方运算。

def est_square(n):
	j = 1
	tmp = n
	while tmp>0:
		tmp -= j
		if tmp == 0:
			return '自然数%d是数%d的平方' %(n,(j+1)/2)
		elif tmp < 0:
			return '自然数%d不是平方数' %n 
		j += 2

if __name__ == '__main__':
	print est_square(9323)
	print est_square(8100)
