#encoding=utf-8

from __future__ import division

'''
two numbers change bigger as the same proportion at the same time,
and the max one is 1
'''

def propotion(num1,num2):
	n1 = min([num1/num2,1])
	n2 = min([num2/num1,1])
	return n1,n2

if __name__ == '__main__':
	print propotion(0.3,0.5)
	print propotion(0.6,0.4)
