import math
import operator

#计算用户的相似性
#余弦相似度
def UserSimilarity(train):#train = dict, key = user, value = dict(item, number);
	_item = dict();
	for user, item in train.items():
		for it, it_v in item.items():
			if it not in _item:
				_item[it] = set();
			_item[it].add(user);
	cnt = dict()
	N = dict()
	for i, user in _item.items():
		for u in user:
			if u not in N:
				N[u]=0;
			N[u] = N[u] + 1
			for v in user:
				if u not in cnt:
					cnt[u]=dict()
				if v not in cnt[u]:
					cnt[u][v] = 0
				if u == v:
					continue
				cnt[u][v] = cnt[u][v] + 1
	W = dict()
	for u, fou in cnt.items():
		if u not in W:
			W[u]=dict()
		for v, cuv in fou.items():
			W[u][v] = cuv / math.sqrt(N[u] * N[v]);
	return W


#通过相似度矩阵进行推荐
#参数说明：user: 用户ID   train:训练集   K: 计算时选前K个相似的
def userCF(user, train, K):#train = dict, key = user, value = dict(item, number);
	W = UserSimilarity(train)
	re = dict()
	has_in = train[user]
	cnt = dict();
	for v, w_uv in sorted(W[user].items(), key = operator.itemgetter(1), reverse = True)[0:K]:#选取前K个相似的用户进行推荐
		for i, ti in train[v].items():
			if i in has_in:
				continue
			if i not in re:
				cnt[i] = 0;
				re[i] = 0.0
			cnt[i] += 1;
			re[i] += w_uv * ti
	for i, ci in cnt.items():
		re[i] /= ci;
	return re