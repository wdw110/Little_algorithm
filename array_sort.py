#encoding=utf-8

#给定一个存放整数的数组，重新排列数组使得数组左边为奇数，右边为偶数。
#要求：空间复杂度O(1)，时间复杂度为O（n）。

def arr_sort(arr):
	i = 0; j = len(arr)-1
	while i<j:
		if arr[i]%2==0 and arr[j]%2==1:
			arr[i],arr[j] = arr[j],arr[i]
		if arr[i]%2==1:
			i += 1
		if arr[j]%2==0:
			j -= 1
	return arr


if __name__ == '__main__':
	arr = [1,3,3,21,5,64,23,213,12]
	print arr_sort(arr)

