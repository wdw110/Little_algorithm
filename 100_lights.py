#encoding=utf-8

#一百个灯泡排成一排，第一轮将所有灯泡打开；第二轮每隔一个灯泡关掉一个，即排在偶数的灯泡都被关掉。第三轮每隔两个灯泡，将开着的灯泡关掉，关掉的灯泡打开。以此类推，第100轮的时候，还有几盏灯泡亮着？你知道答案吗？

def lights(N): #N为灯泡总数
	arr = [1 for i in range(N)]
	for i in range(1,N):
		for j in range(-1,len(arr),i):
			arr[j] = 0 - arr[j]
	return arr

if __name__ == '__main__':
	a = lights(100)
	n = 0
	for i in range(len(a)):
		if a[i]== -1:
			n += 1
			print '亮着的灯泡为：%d' %(i+1)
	print '总共的灯泡数为%d个' %n