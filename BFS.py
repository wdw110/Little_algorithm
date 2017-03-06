# encoding=utf-8
# author: wdw110
# algorithm: BFS(广度优先搜索方法-最短路径问题)
#（1）将起始节点放入队列尾部
#（2）While(队列不为空）
#    取得并删除队列首节点Node
#    处理该节点Node
#    把Node的未处理相邻节点加入队列尾部

import numpy as np

data = np.array([0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0]).reshape(5,5)

color = -np.ones((5,5))  #颜色标识：-1为白色，0位灰色，1为黑色

def find_node(m,n): # m,n:位置坐标
	'''找出与该节点相关的所有节点'''
	res = []
	color[m,n] = 1
	if 0 <= m+1 < 5:
		if color[m+1,n] < 1 and data[m+1,n] == 0:
			color[m+1,n] = 0
			res.append((m+1,n))
	for i in [-1,1]:
		if 0 <= n+i < 5:
			if color[m,n+i] < 1 and data[m,n+i] == 0:
				color[m,n+i] = 0
				res.append((m,n+i))
	return res


def bfs():
	first_node = (0,0) #起始位置
	end_node = (4,4)   #结束位置
	obj = {}  #记录k:当前节点，v:父节点
	res = []  #最短路径
	queue = []
	queue.append(first_node)
	obj[first_node] = ''
	while queue:
		node = queue[0]
		queue.pop(0)
		arr_node = find_node(node[0],node[1])
		for nn in arr_node:
			obj[nn] = node
		if end_node in arr_node:
			tmp = (4,4)
			while tmp:
				res.insert(0, tmp)
				tmp = obj[tmp]
			return res
		queue.extend(arr_node)

			
if __name__ == '__main__':
	a = bfs()
	print '迷宫的路线为：',a