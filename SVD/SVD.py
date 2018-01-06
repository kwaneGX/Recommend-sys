from numpy import *
from numpy import linalg as la

#欧式距离
def ecludSim(inA, inB):
    return 1.0/(1.0+ la.norm(inA - inB))

#余弦距离
def cosSim(inA, inB):
    num = float(inA.T*inB)
    denom = la.norm(inA)*la.norm(inB)
    return 0.5+0.5*(num/denom)

#SVD推荐
def svdEst(dataMat, user, simMeas, item, cnt, U, Sigma, VT):
    if item not in cnt: return 0;
    n = shape(dataMat)[1]
    simTotal = 0.0; ratSimTotal = 0.0
    Sig4 = mat(eye(4)*Sigma[:4]) #arrange Sig4 into a diagonal matrix
    xformedItems = dataMat.T * U[:,:4] * Sig4.I  #create transformed items
    for j in range(n):
        if j not in cnt: continue;
        userRating = dataMat[user,j]
        if userRating == 0 or j==item: continue
        similarity = simMeas(xformedItems[item,:].T,xformedItems[j,:].T)
        #print 'the %d and %d similarity is: %f' % (item, j, similarity)
        simTotal += similarity
        ratSimTotal += similarity * userRating
    if simTotal == 0: return 0
    else: return ratSimTotal/simTotal

#itemCF
def standEst(dataMat, user, simMeas, item, cnt, U, Sigma, VT):
    n = shape(dataMat)[1]
    simTotal = 0.0; ratSimTotal = 0.0
    for j in range(n):
        userRating = dataMat[user,j]
        if userRating == 0:continue
        overLap = nonzero(logical_and(dataMat[:,item].A>0,dataMat[:,j].A>0))[0]
        if len(overLap) == 0:similarity = 0
        else:similarity = simMeas(dataMat[overLap,item],dataMat[overLap,j])
        simTotal += similarity
        ratSimTotal += similarity * userRating
    if simTotal == 0:return 0
    else: return ratSimTotal/simTotal

#推荐
def recommend(dataMat, user, cnt, N=4, simMeas = cosSim, estMethod = standEst):
    unratedItems = nonzero(dataMat[user,:].A == 0)[1]
    if len(unratedItems) == 0:return "you rated everything"
    itemScores = []
    U,Sigma,VT = la.svd(dataMat) #直接进行分解
    for item in unratedItems:
        estimateScore = estMethod(dataMat, user, simMeas, item, cnt, U, Sigma, VT)
        itemScores.append((item,estimateScore))
    return sorted(itemScores,key=lambda jj: jj[1],reverse=True)[:N]

#通过SVD进行推荐
def SVD(userID, train, N, way = svdEst, diff = cosSim):
	n = max(train.keys());
	t = list();
	for user, item in train.items():
		t.append(max(item.keys()));
	m = max(t);
	data_Mat = mat(zeros((n, m)));
	cnt = set()
	for user, item in train.items():
		for it, score in item.items():
			data_Mat[user - 1, it - 1] = score;
			if it - 1 not in cnt:
                            cnt.add(it - 1);
	outcome = recommend(data_Mat, userID - 1, cnt, N, diff, way)
	return outcome;


