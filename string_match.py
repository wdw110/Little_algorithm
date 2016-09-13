#encoding=utf-8

#假设两个字符串中所含有的字符和个数都相同我们就叫这两个字符串匹配，
#比如：abcda和adabc,由于出现的字符个数都是相同，只是顺序不同，所以这两个字符串是匹配的。要求高效。

#思路：假定字符串中都是ASCII字符。用一个数组来计数，前者加，后者减，全部为0则匹配。

def str_match(s1,s2):
	obj = dict([(i,0) for i in range(256)]) #构造初始化数组

	if len(s1) == len(s2):
		for i in range(len(s1)):
			a1 = ord(s1[i]); a2 = ord(s2[i])
			obj[a1] += 1
			obj[a2] -= 1
		for value in obj.values():
			if value != 0:
				return '两个字符串不匹配'

		return '两个字符串匹配'
	else:
		return '两个字符串不匹配'

if __name__ == '__main__':
	s1 = 'sdlfj'
	s2 = 'ljdfs'
	print str_match(s1,s2)