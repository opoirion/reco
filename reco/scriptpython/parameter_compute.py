#! -*- coding:utf-8 -*- 
#print exp(-0.5*pow(MIN of: [Math.max(arcDistance([45.7510518, 4.8268188](=doc value),[45.76749, 4.83433](=origin)) - 4000.0(=offset), 0)],2.0)/2885390.081777927)

from reco_tools import *


log=LogisticRegression()
clf=ExtraTreesClassifier(bootstrap=True,oob_score=True,n_estimators=5000)
clr=ExtraTreesRegressor(bootstrap=True,oob_score=True,n_estimators=5000)



GoldenNumber=-0.0124077324


def main():
	with open('../data/data_saved_v2_s100000','r') as f:
		duration_diff,occurence,time_diff,spatial_diff,position=cPickle.load(f)
	print sp.mean(position),sp.std(position)
	#return
	#print duration_diff
	occurence=stats.threshold(sp.asarray(occurence).astype('float'),threshmin=0.5,newval=0.5)
	time_diff=stats.threshold(sp.asarray(time_diff).astype('float'),threshmin=0.5,newval=0.5)
	duration_diff=stats.threshold(sp.asarray(duration_diff).astype('float'),threshmin=0.5,newval=0.5)
	
	occurence=sp.exp(GoldenNumber*occurence)
	time_diff=sp.exp(GoldenNumber*time_diff)
	duration_diff=sp.exp(GoldenNumber*duration_diff)
	
	spatial_diff=stats.threshold(sp.asarray(spatial_diff).astype('float'),threshmin=0.0001,newval=0.0001)
	spatial_diff=sp.exp(GoldenNumber*spatial_diff)
	
	expr="spatial_diff,duration_diff,occurence,time_diff,position"
	legend=expr.split(',')[:-1]
	M=sp.array(eval(expr)).astype('float').T
	
	#M=sp.array([spatial_diff,position]).astype('float').T
	
	#M=sp.array([spatial_diff,time_diff]).astype('float').T
	
	M=sp.asarray(filter(lambda x:not sp.isnan(x).any() and (x>0).all(),M))
	position=M.T[-1][:]
	M=M.T[:-1].T
	#print M[:100]
	#return
	#for m in M:print m
	#for m in M:print m
	#M=sp.exp(GoldenNumber*M)
	#M[0]=sp.exp(0.5*M[0])
	
	#M=1.0/M
	#print '\n'
	#print M[:10]
	#return
	#
	M=preprocessing.scale(M)
	print '\n'
	#print M[:100]
	position_bin=map(lambda x:int(x>30),position)
	position=position**2
	print len(position),M.shape
	
	OLSreg(position,M,namelist=legend)
	GLMreg(position_bin,M,namelist=legend)
	
	print '#### go log fiting ####';t=time.time()
	log.fit(M,position_bin)
	print 'done in :{0} s'.format(time.time()-t)
	print 'score:',log.score(M,position_bin)
	for f in zip(legend,log.coef_[0]):
		print f
	#return
	print '#### go clf fiting ####';t=time.time()
	clf.fit(M,position_bin)
	print 'done in :{0} s'.format(time.time()-t)
	print 'score:',clf.score(M,position_bin)
	print 'oob score:',clf.oob_score_
	for f in zip(legend,clf.feature_importances_):
		print f
	
	
	print '#### go clr fiting ####';t=time.time()
	clr.fit(M,position)
	print 'done in :{0} s'.format(time.time()-t)
	print 'score:',clr.score(M,position_bin)
	print 'oob score:',clr.oob_score_
	for f in zip(legend,clr.feature_importances_):
		print f
	
	
	return
	pca=decomposition.PCA(n_components=2,whiten=False)
	pca.fit(M[:1000])
	Sum=sp.absolute(pca.components_[0]).sum()
	print 'spatial_diff\tduration_diff\toccurence\ttime_diff'
	print 'sum:',Sum
	print 'components 0:', pca.components_[0]/Sum
	print 'components 1:', pca.components_[1]/Sum
	print 'explained variance:',pca.explained_variance_ratio_
	
	return
	pylab.subplot(2,2,1)
	pylab.boxplot(spatial_diff)
	pylab.ylabel('distance en coordonnees')
	pylab.subplot(2,2,2)
	pylab.boxplot(filter(lambda x:x!=None,time_diff))
	pylab.ylabel('time proximity (day)')
	pylab.subplot(2,2,3)
	pylab.boxplot(filter(lambda x:x!=None,occurence))
	pylab.ylabel('occurence (nb time)')
	pylab.subplot(2,2,4)
	pylab.boxplot(filter(lambda x:x!=None and x<2900000,duration_diff))
	pylab.ylabel('duration (day)')
	pylab.show()
	raw_input()
	
	
	
	

if __name__=='__main__':
	main()