#encoding=utf-8

def Insert_sort(arr): #直接插入排序(Straight Insertion Sort)
#基本思路：将一个记录插入到已排序好的有序表中，从而得到一个新，记录数增1的有序表。
#即：先将序列的第1个记录看成是一个有序的子序列，然后从第2个记录逐个进行插入，直至整个序列有序为止。
	print '插入排序方法如下：'
	tmp = list(arr)
	n = len(tmp)
	for i in range(1,n):
		print i,tmp
		tt = tmp[i]
		j = i-1
		while j>=0 and tmp[j]>tt:
			tmp[j+1] = tmp[j]
			j -= 1
		tmp[j+1] = tt
	return tmp

def Shell_sort(arr):
#基本思路：先将整个待排序的记录序列分割成为若干子序列分别进行直接插入排序，
#待整个序列中的记录“基本有序”时，再对全体记录进行依次直接插入排序。
	print '希尔排序方法如下：'
	tmp = list(arr)
	n = len(tmp)
	d = n/2
	while d>=1:
		for i in range(d,n):
			tt = tmp[i]
			j = i - d
			while j>=0 and tmp[j]>tt:
				tmp[j+d] = tmp[j]
				j -= d
			tmp[j+d] = tt
			print i,tmp	
		d /= 2
	return tmp

def Select_sort(arr):
#基本思路：在要排序的一组数中，选出最小（或者最大）的一个数与第1个位置的数交换；然后在剩下的数当中再找最小
#（或者最大）的与第2个位置的数交换，依次类推，直到第n-1个元素（倒数第二个数）和第n个元素（最后一个数）比较为止。
	print '选择排序方法如下：'
	tmp = list(arr)
	n = len(tmp)
	for i in range(n):
		print i,tmp
		for j in range(i+1,n):
			if tmp[i]>tmp[j]:
				tmp[i],tmp[j] = tmp[j],tmp[i]
	return tmp

def Select_two_sort(arr):
#基本思路：简单选择排序，每趟循环只能确定一个元素排序后的定位。我们可以考虑改进为每趟循环确定两个元素（当前趟最大和最小记录）的位置,
#从而减少排序所需的循环次数。改进后对n个数据进行排序，最多只需进行[n/2]趟循环即可。
	print '二元选择排序方法如下：'
	tmp = list(arr)
	n = len(tmp)
	for i in range(n/2):
		print i,tmp
		max_t = i; min_t = i
		for j in range(i+1,n-i):
			if tmp[max_t] < tmp[j]: max_t = j; continue
			if tmp[min_t] > tmp[j]: min_t = j
		tmp[i],tmp[min_t] = tmp[min_t],tmp[i]
		tmp[n-i-1],tmp[max_t] = tmp[max_t],tmp[n-i-1]
	return tmp

def Bubble_sort(arr):
#基本思路：在要排序的一组数中，对当前还未排好序的范围内的全部数，自上而下对相邻的两个数依次进行比较和调整，
#让较大的数往下沉，较小的往上冒。即：每当两相邻的数比较后发现它们的排序与排序要求相反时，就将它们互换。
	print '冒泡排序方法如下：'
	tmp = list(arr)
	n = len(tmp)
	for i in range(n):
		print i,tmp
		for j in range(n-i-1):
			if tmp[j+1]<tmp[j]:
				tmp[j+1],tmp[j] = tmp[j],tmp[j+1]
	return tmp

def 


if __name__ == '__main__':
	arr = [10,23,1,321,5,34,10,11,2,43]
	print Insert_sort(arr)
	print Bubble_sort(arr)
	print Select_sort(arr)
	print Shell_sort(arr)
	print Select_two_sort(arr)

