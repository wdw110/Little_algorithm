#encoding=utf-8

from __future__ import division
import re
import time
import math
import jieba
import MySQLdb
import numpy as np 

start = time.time()
tf = {} #{id:[{},{},..],...}
idf_bre = {}
idf_aft = {}
tv_data = []  #新电视剧的变量数据
score_mat = {} #电视剧得分矩阵{id:[{},{}...],...}
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
	score_mat.setdefault(k,[])
	for j in tmp[i][1:]:
		obj = {}
		if len(j):
			for ss in j.split(','):
				tmp_arr = ss.split(':')
				obj[int(tmp_arr[0])] = tmp_arr[1] 
 		score_mat[k].append(obj)


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
	tv_data[i] = list(tv_data[i])
	key = tv_data[i][0]
	arr = tv_data[i][1:]
	tmp = []  #每个电视剧的所有关键词
	dim_tmp = [] #每个电视剧的每个维度的关键词统计[[{},{}..],..]
	if key not in score_mat:
		tv_sum += 1 #所有电视剧的数量
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
			if key not in score_mat:
				idf_bre[ww] += 1 

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
score_mat_new = dict(score_mat,**dat) #将新剧和老剧的得分合并


#将结果和中间数据保存到数据库中
for key in dat:
	res = tv_sim(key, score_mat_new)
	sim_arr = [i[0] for i in res.values()]
	if key not in score_mat:
		sql = 'insert into ad_tv_cos values ("%d","%s","%s","%s")' %(key,str(res),str(sim_arr),tv_data[2])
		cursor.execute(sql)
		db.commit()


for i in range(len(tv_data)):
	tv_id = tv_data[i][0]
	sql = 'update ad_tv_lib set is_old=%d where id=%d' %(1,int(tv_id))
	cursor.execute(sql)
	db.commit()

vv = []
for key,tv_arr in tf.items():
	tmp = []
	tmp.append(int(key))
	for tv_obj in tv_arr:
		ss = ';'.join([k.encode('utf-8')+':'+str(v) for k,v in tv_obj.items()])
		tmp.append(ss)
	if key not in score_mat:
		vv.append(tuple(tmp))
sql = 'insert into ad_tv_recom_tf values(%s,%s,%s,%s,%s,%s,%s)'
cursor.executemany(sql,vv)
db.commit()

delete = 'delete from ad_tv_recom_idf'
cursor.execute(delete)
db.commit()

tmp_ll = list(idf_bre.items())
vv = [(i+1,tmp_ll[i][0],tmp_ll[i][1],tv_sum) for i in range(len(tmp_ll))]
sql = 'insert into ad_tv_recom_idf values(%s,%s,%s,%s)'
cursor.executemany(sql,vv)
db.commit()


delete = 'delete from ad_tv_recom_score_matrix'
cursor.execute(delete)
db.commit()
vv = []
for tv_id,np_arr in score_mat_new.items():
	nn = 0
	res = []
	res.append(tv_id)
	for arr in var_stat:
		tmp = np_arr[nn:(nn+len(arr))]
		nn +=  len(arr)
		ss = ','.join([str(i)+':'+str(tmp[i]) for i in np.nonzero(tmp)[0]])
		res.append(ss)
	vv.append(tuple(res))
sql = 'insert into ad_tv_recom_score_matrix values (%s,%s,%s,%s,%s,%s,%s)'
cursor.executemany(sql,vv)
db.commit()

cursor.close()
db.close()

