import math
import operator


#求物品的相似度矩阵
#余弦相似度
def itemSimilarity(train):#train = dict, key = user, value = dict(item, number);
	cnt = dict();
	N = dict();
	for u, item in train.items():
		for i in item:
			if i not in N:
				N[i] = 0;
			N[i] = N[i] + 1;
			for j in item:
				if i == j:
					continue;
				if i not in cnt:
					cnt[i] = dict();
				if j not in cnt[i]:
					cnt[i][j] = 0;
				cnt[i][j] = cnt[i][j] + 1;
	W = dict();
	for i, foi in cnt.items():
		if i not in W:
			W[i] = dict();
		for j, cij in foi.items():
			W[i][j] = cij / math.sqrt(N[i] * N[j]);
	return W;

#通过相似度矩阵进行推荐
#参数说明：user: 用户ID   train:训练集   K: 计算时选前K个相似的
def itemCF(user, train, K):#train = dict, key = user, value = dict(item, number);
	W = itemSimilarity(train);
	re = dict();
	has_in = train[user];
	cnt = dict();
	for i, pi in has_in.items():
		for j, wij in sorted(W[i].items(), key = operator.itemgetter(1), reverse = True)[0:K]:#选和当前物品相似度排名前K个
			if j in has_in:
				continue;
			if j not in re:
				re[j] = 0.0;
				cnt[j] = 0;
			cnt[j] += 1;
			re[j] += pi * wij;
	for i, ci in cnt.items():
		re[i] /= ci;
	return re;