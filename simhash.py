#encoding=utf-8

##simhash是google用来处理海量文本去重的算法。simhash最牛逼的一点就是将一个文档，最后转换成一个64位的字节，暂且称之为特征字，
##然后判断重复只需要判断他们的特征字的距离是不是<n（根据经验这个n一般取值为3），就可以判断两个文档是否相似。

class Hash(object):
	"""docstring for Hash"""
	def additiveHash(slef, String, prime): #prime是任意质数
		
		

