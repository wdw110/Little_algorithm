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
		if max_t==i:
			tmp[n-i-1],tmp[max_t] = tmp[max_t],tmp[n-i-1]
			tmp[i],tmp[min_t] = tmp[min_t],tmp[i]
		else:
			tmp[i],tmp[min_t] = tmp[min_t],tmp[i]
			tmp[n-i-1],tmp[max_t] = tmp[max_t],tmp[n-i-1]
	return tmp

def adjust_heap(arr, i, length):
	tmp = arr[i]
	child = 2*i+1
	while child < length:
		if child+1<length and arr[child]<arr[child+1]:
			child += 1
		if arr[i] < arr[child]:
			arr[i] = arr[child]
			i = child
			child = 2*i+1
		else: break
		arr[i] = tmp

def build_heap(arr, length):
#建立堆这种数据结构
	for i in range(0,length/2)[::-1]:
		adjust_heap(arr,i,length)

def Heap_sort(arr):
#基本思路：一种树形选择排序，是对直接选择排序的有效改进。利用堆这种数据结构所设计的一种排序算法。堆积是一个近似
#完全二叉树的结构，并同时满足堆积的性质：即子结点的键值或索引总是小于（或者大于）它的父节点。
	print '堆排序方法如下：'
	tmp = list(arr)
	n = len(tmp)
	build_heap(tmp, n)
	for i in range(n)[::-1]:
		tmp[0],tmp[i] = tmp[i],tmp[0]
		adjust_heap(tmp, 0, i)
		print i,tmp
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
#对冒泡排序常见的改进方法是加入一标志性变量exchange，用于标志某一趟排序过程中是否有数据交换，
#如果进行某一趟排序时并没有进行数据交换，则说明数据已经按要求排列好，可立即结束排序，避免不必要的比较过程。
def Bubble_pos_sort(arr):
#基本思路：设置一标志性变量pos,用于记录每趟排序中最后一次进行交换的位置。
#由于pos位置之后的记录均已交换到位,故在进行下一趟排序时只要扫描到pos位置即可。
	print 'pos改进的冒泡排序方法如下：'
	tmp = list(arr)
	lat = len(tmp)-1
	while lat>0:
		pos = 0
		print lat,tmp
		for i in range(lat):
			if tmp[i]>tmp[i+1]:
				pos = i
				tmp[i],tmp[i+1] = tmp[i+1],tmp[i]
		lat = pos
	return tmp

def Bubble_two_sort(arr):
#基本思路：传统冒泡排序中每一趟排序操作只能找到一个最大值或最小值,我们考虑利用在每趟排序中进行正向
#和反向两遍冒泡的方法一次可以得到两个最终值(最大者和最小者) , 从而使排序趟数几乎减少了一半。
	print 'two改进的冒泡排序方法如下：'
	tmp = list(arr)
	n = len(tmp)
	low = 0; high = n-1
	while low<high:
		print low,tmp
		for i in range(1,high)[::-1]:
			if tmp[i-1]>tmp[i]:
				tmp[i-1],tmp[i] = tmp[i],tmp[i-1]
		for i in range(high):
			if tmp[i]>tmp[i+1]:
				tmp[i],tmp[i+1] = tmp[i+1],tmp[i]
		low += 1; high -= 1
	return tmp

def Quick_sort(arr, low, high):
#基本思路：1）选择一个基准元素,通常选择第一个元素或者最后一个元素,
#2）通过一趟排序讲待排序的记录分割成独立的两部分，其中一部分记录的元素值均比基准元素值小。另一部分记录的 元素值比基准值大。
#3）此时基准元素在其排好序后的正确位置
#4）然后分别对这两部分记录用同样的方法继续进行排序，直到整个序列有序。
	if low >= high:
		return arr
	left = low
	right = high
	pivotkey = arr[high]
	while low < high:
		print low,high,arr
		while low<high and arr[low]<=pivotkey: 
			low += 1
		arr[high] = arr[low]
		while low<high and arr[high]>=pivotkey: 
			high -= 1
		arr[low] = arr[high]
	arr[high] = pivotkey
	Quick_sort(arr, left, low-1)
	Quick_sort(arr, low+1, right)
	return arr

def merge(left, right):
	i, j = 0, 0
	result = []
	while i<len(left) and j<len(right):
		if left[i]<=right[j]:
			result.append(left[i])
			i += 1
		else:
			result.append(right[j])
			j += 1
	result += left[i:]
	result += right[j:]
	print result
	return result

def Merge_sort(arr):
#基本思路：归并（Merge）排序法是将两个（或两个以上）有序表合并成一个新的有序表，
#即把待排序序列分为若干个子序列，每个子序列是有序的。然后再把有序子序列合并为整体有序序列。
	if len(arr)<=1:
		return arr
	num = len(arr)/2
	left = Merge_sort(arr[:num])
	right = Merge_sort(arr[num:])
	return merge(left, right)

import math
def Radix_sort(arr,radix=10):
#基本思路：基数排序（radix sort）属于“分配式排序”（distribution sort），又称“桶子法”（bucket sort）或bin sort，
#顾名思义，它是透过键值的部份资讯，将要排序的元素分配至某些“桶”中，藉以达到排序的作用，基数排序法是属于稳定性的排序，
#其时间复杂度为O (nlog(r)m)，其中r为所采取的基数，而m为堆数，在某些时候，基数排序法的效率高于其它的稳定性排序法。
	print '基数排序方法如下：'
	tmp = list(arr)
	k = int(math.ceil(math.log(max(tmp), radix)))
	bucket = [[] for i in range(radix)]
	for i in range(1,k+1):
		for j in tmp:
			bucket[j/radix**(i-1)%radix].append(j)
		print i,tmp
		del tmp[:]
		for k in bucket:
			tmp += k
			del k[:]
	return tmp


if __name__ == '__main__':
	arr = [10,23,1,321,5,34,10,11,2,43]
	print Insert_sort(arr)
	print Shell_sort(arr)
	print Select_sort(arr)
	print Select_two_sort(arr)
	print Heap_sort(arr)
	print Bubble_sort(arr)
	print Bubble_pos_sort(arr)
	print Bubble_two_sort(arr)
	print '快速排序方法如下：'
	print Quick_sort(arr,0,len(arr)-1)
	arr = [10,23,1,321,5,34,10,11,2,43]
	print '归并排序方法如下：'
	print Merge_sort(arr)
	print Radix_sort(arr)


