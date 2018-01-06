#计算物品间评分差距
def getDiffs(train):
	diffs = dict();
	cnt = dict();
	for users, item in train.items():
		#print(users);
		for item1, rating1 in item.items():
			if item1 not in diffs:
				diffs[item1] = dict();
			if item1 not in cnt:
				cnt[item1] = dict();
			for item2, rating2 in item.items():
				if item2 not in diffs[item1]:
					diffs[item1][item2] = 0.0;
				if item2 not in cnt[item1]:
					cnt[item1][item2] = 0;
				diffs[item1][item2] += rating1 - rating2;
				cnt[item1][item2] += 1;
	for item1, diff in diffs.items():
		for item2, rating in diff.items():
			diff[item2] /= cnt[item1][item2];
	return diffs,cnt;

#用户评分预测
def SlopeOneRecommend(userNo, train):
	#判断userNo有没有历史评价
	if not train[userNo]:
		return "has no item in user " + str(userNo);
	[diffs,cnt] = getDiffs(train);
	#print("cacled diffs...");
	rated = {};
	unrated = set();
	predict = dict();
	c = {};
	for item, it in diffs.items():
		if item in train[userNo]:
			rated[item] = train[userNo][item];
		else:
			unrated.add(item);
	for tarItem in unrated:
	#	print(tarItem);
		if tarItem not in predict:
			predict[tarItem] = 0.0;
		if tarItem not in c:
			c[tarItem] = 0;
		for item, rate in rated.items():
		#	print(tarItem,item);
			if tarItem not in cnt:
				continue;
			if item not in cnt[tarItem]:
				continue;
			c[tarItem] += cnt[tarItem][item];
			predict[tarItem] += cnt[tarItem][item] * (rate - diffs[item][tarItem]);
		if c[tarItem] == 0:
			continue;
		predict[tarItem] /= c[tarItem];
	return predict;