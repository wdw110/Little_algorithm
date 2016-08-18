#encoding=utf-8

#轮盘赌选择法的python实现
#p:为一个概率向量，表示各个元素发生的概率，其和是1

from __future__ import division
import random
import numpy as np

def create_p(n): #n为向量p的维数
	tmp = np.array([random.random() for i in range(n)])
	p = tmp/sum(tmp)
	return p

def selection_p(p):
	accumulate_p = []
	for i in range(1,len(p)+1):
		accumulate_p.append(sum(p[0:i]))

	point = random.random()
	for i in range(len(accumulate_p)):
		if accumulate_p[i]>point:
			break
	return point,accumulate_p,p[i]

if __name__ == '__main__':
	p = create_p(6)
	print p
	print selection_p(p)