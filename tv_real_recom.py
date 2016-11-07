#encoding=utf-8

from __future__ import division
import re
import time
import math
import jieba
import MySQLdb
import numpy as np 

start = time.time()
tf = {}
idf_bre = {}
idf_aft = {}
tv_data = []  #新电视剧的变量数据
score_mat = {}
tags = {} #标签库
weight = [5,2,1,1,1,1]
rules = u'，|；|。|、|（|）|/|\[|\]| |\(|\)|\*|\+|,|-|\.|:|;|\||<|=|>'

db = MySQLdb.connect(host='121.41.17.212',user='yxb',passwd='123456',db='yxb',charset='utf8') #打开数据库连接
cursor = db.cursor() #使用cursor()方法获取操作游标

sql1 = 'select * from ad_tv_recom_idf'
cursor.execute(sql1)
tmp =cursor.fetchall()

tv_sum = tmp[0][3] #历史总电视剧数

for i in range(len(tmp)):
	arr = tmp[i]
	idf_bre[arr[1]] = arr[2]

sql2 = 'select * from ad_tv_recom_var_stat'
cursor.execute(sql2)
tmp = cursor.fetchall()
var_stat = [word.split(',') for word in tmp[0]] #各维度的词统计


sql3 = 'select * from ad_tv_recom_score_matrix'
cursor.execute(sql3)
tmp = cursor.fetchall()
for i in range(len(tmp)):
	k = int(tmp[i][0])
	score_mat[k] = [eval(j) for j in tmp[i][1:]]

sql4 = 'select tag from ad_type_lib1'
cursor.execute(sql4)
tmp = cursor.fetchall()
for word in tmp:
	tags[word[0]] = 1


dims = ['id','types','description_one','director','main_actors','scriptwritter','production']
sql = "select %s from ad_tv_lib where is_old=%d" %(', '.join(dims),0)
cursor.execute(sql)
tv_data = list(cursor.fetchall())

def find_tag(sentence): #sentence为电视剧的描述信息
	seg = jieba.cut(sentence)
	res = {}
	for word in seg:
		word = word
		if tags.get(word):
			res.setdefault(word,1)
	return ','.join(res.keys())

for i in range(len(tv_data)):
	tv_sum += 0 #tv_sum += 1  #所有电视剧的数量
	tv_data[i] = list(tv_data[i])
	key = tv_data[i][0]
	arr = tv_data[i][1:]
	tmp = []  #每个电视剧的所有关键词
	dim_tmp = [] #每个电视剧的每个维度的关键词统计[[{},{}..],..]
	if not arr[1]: 
		arr[1] = ''
		tv_data[i][2] = ''
	else: 
		arr[1] = find_tag(arr[1])
		tv_data[i][2] = arr[1]
	for j in range(len(arr)):
		obj = {}
		if not arr[j]: 
			wd = u''
		else:
			wd = arr[j]
		words = re.sub(rules,';',wd).split(';')
		words = list(set(words))
		if u'' in words:
			words.remove(u'')
		tmp.extend(words) 
		for word in words:
			obj.setdefault(word, 0)
			obj[word] += 1
		dim_tmp.append(obj)
	n = len(tmp) #每个电视剧的总词数
	for l in range(len(dim_tmp)):
		obj_j = dim_tmp[l]
		for k in obj_j:
			obj_j[k] /= n
			if k not in var_stat[l]: #判断新剧的关键词是否在历史关键词库中
				var_stat[l].append(k)
	tf[key] = dim_tmp
	for ww in list(set(tmp)):
		if not idf_bre.has_key(ww):
			idf_bre[ww] = 1
		else:
			idf_bre[ww] += 0  #idf_bre[ww] += 1

for key in idf_bre:
	idf_aft[key] = math.log10(tv_sum/idf_bre[key])

#对历史电视剧的得分矩阵重新计算
for key in score_mat:
	tmp_arr = score_mat[key]
	tmp = []
	for i in range(len(var_stat)):
		mat = tmp_arr[i]
		tt = np.zeros(len(var_stat[i]))
		tt[mat.keys()] = mat.values()
		tmp.extend(list(tt))
	score_mat[key] = np.array(tmp)

#计算电视剧矩阵得分
def tv_score(weight, tf, idf):
	res = {}
	row = sum([len(v) for v in var_stat])
	for i in tf:
		tv_arr = tf[i]
		mm = 0 #每个词的位置
		res.setdefault(i,np.zeros(row))
		for j in range(len(tv_arr)):
			if j>0: mm += len(var_stat[j-1]) 
			for word,value in tv_arr[j].items():
				score = weight[j]*value*idf[word]
				nn = var_stat[j].index(word) + mm
				res[i][nn] = score
	return res

def cos_distance(vec1, vec2):
	v11 = vec1*vec1
	v12 = vec1*vec2
	v22 = vec2*vec2
	mer = sum(v12[v12>0])
	denominator = math.sqrt(sum(v11[v11>0])) + math.sqrt(sum(v22[v22>0]))
	if not denominator:
		return 0
	return mer/denominator

def tv_sim(tv_id,data): #tv_id:要计算的电视剧(1,2,3...)，data:电视剧得分矩阵({1:[],2:[]})
	res = []
	vec1 = data[tv_id]
	for key,tv_arr in data.items():
		cos = cos_distance(vec1,tv_arr)
		res.append([key,cos])
	return dict(enumerate(sorted(res,key=lambda x:x[1],reverse=True)[0:100]))

dat = tv_score(weight,tf,idf_aft)
score_mat = dict(score_mat,**dat) #将新剧和老剧的得分合并


#将结果和中间数据保存到数据库中
for key in dat:
	res = tv_sim(key, score_mat)
	sim_arr = [i[0] for i in res.values()]
	sql = 'insert into ad_tv_cos values ("%d","%s","%s","%s")' %(key,str(res),str(sim_arr),'')
	cursor.execute(sql)
	db.commit()
print 1

for i in range(len(tv_data)):
	tv_id = tv_data[i][0]
	sql = 'update ad_tv_lib set is_old=%d where id=%d' %(1,int(tv_id))
	cursor.execute(sql)
	db.commit()
print 2

delete = 'delete from ad_tv_recom_idf'
cursor.execute(delete)
db.commit()
n = 1
for k,v in idf_bre.items():
	sql = 'insert into ad_tv_recom_idf values ("%d","%s","%d","%d")' %(n,k,int(v),int(tv_sum))
	cursor.execute(sql)
	db.commit()
	n += 1
print 3
'''
delete = 'delete from ad_tv_recom_score_matrix'
cursor.execute(delete)
db.commit()
'''
for tv_id,np_arr in score_mat.items():
	nn = 0
	res = []
	for arr in var_stat:
		tmp = np_arr[nn:(nn+len(arr))]
		nn +=  len(arr)
		res.append(str(dict(zip(np.nonzero(tmp)[0],tmp[np.nonzero(tmp)[0]]))))
	sql = 'insert into ad_tv_recom_score_matrix values ("%d","%s","%s","%s","%s","%s","%s")' %(tv_id,res[0],res[1],res[2],res[3],res[4],res[5])
	cursor.execute(delete)
	db.commit()
print 4

