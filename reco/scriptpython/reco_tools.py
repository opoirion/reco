import pylab
import cPickle
import scipy as sp
from sklearn import decomposition
from scipy.cluster.vq import whiten
from sklearn import preprocessing
from scipy import stats
import statsmodels.api as sm
from sklearn.ensemble import ExtraTreesClassifier,ExtraTreesRegressor
import time
from sklearn.linear_model import LogisticRegression

import sys,os

########### path ##########
pathdata='../data/'
###########################


def OLSreg(y,x,vardic=False,graph=True,xlabel='',shuffle=False,namelist=False,return_coefs=False,mode=1,pathsave=''):
	X=sp.asarray([sp.ones(x.shape[0]).tolist()]+x.T.tolist()).T
	if shuffle:
		if mode==1:y=list(y);random.shuffle(y)
		elif mode==2:y=(max(y)-min(y))*sp.random.random(len(y))+min(y)
	#print X
	res=sm.OLS(y,X).fit()
	if return_coefs:
		return res.params(),res.pvalues()
	if vardic:
		namelist=vardic.items()
		namelist.sort(key=lambda i:i[1])
		namelist=['const']+[n[0] for n in namelist]
		#print len(namelist),X.shape
	if  namelist:
		print res.summary(xname=['intercept']+namelist)
		
	else:print res.summary()
	if graph:
		import pylab
		f1=sm.graphics.qqplot(res.resid/y, scale=1, fit=False, line='r', ax=None)
		if pathsave:f1.savefig(pathsave+xlabel+'_qqplot.png')
		f2=pylab.figure()
		pylab.scatter(y,res.resid/y,c='g')
		pylab.xlabel('Full OLS model error normed (Y-Yp)/Y '+xlabel)
		if pathsave:f2.savefig(pathsave+xlabel+'_error_normed.png')
		f3=pylab.figure()
		pylab.scatter(y,res.resid,c='r')
		pylab.xlabel('Full OLS model error (Y-Yp) '+xlabel)
		if pathsave:f3.savefig(pathsave+xlabel+'_normal.png')


		pylab.show()
		raw_input()
	return res

def GLMreg(y,x,vardic=False,family='Binomial',graph=False,xlabel='',shuffle=False,return_coefs=False,namelist=False,mode=1,pathsave=''):
	family=sm.families.__dict__[family]()
	X=sp.asarray([sp.ones(x.shape[0]).tolist()]+x.T.tolist()).T
	if shuffle:
		if mode==1:y=list(y);random.shuffle(y)
		elif mode==2:y=(max(y)-min(y))*sp.random.random(len(y))+min(y)
	#print X
	res=sm.GLM(y,X,family=family).fit()
	if return_coefs:
		return res.params,res.pvalues
	if vardic:
		namelist=vardic.items()
		namelist.sort(key=lambda i:i[1])
		namelist=['const']+[n[0] for n in namelist]
		#print len(namelist),X.shape
	if  namelist:
		print res.summary(xname=['intercept']+namelist)
		
	else:print res.summary()
	if graph:
		import pylab
		f1=sm.graphics.qqplot(res.resid_response/y, scale=1, fit=False, line='r', ax=None)
		if pathsave:f1.savefig(pathsave+xlabel+'_qqplot.png')
		f2=pylab.figure()
		pylab.scatter(y,res.resid_response/y,c='g')
		pylab.xlabel('Full OLS model error normed (Y-Yp)/Y '+xlabel)
		if pathsave:f2.savefig(pathsave+xlabel+'_error_normed.png')
		f3=pylab.figure()
		pylab.scatter(y,res.resid_response,c='r')
		pylab.xlabel('Full OLS model error (Y-Yp) '+xlabel)
		if pathsave:f3.savefig(pathsave+xlabel+'_normal.png')


		pylab.show()
		raw_input()
		
		
def load_rdic(rpath='ref_rubric_v1',pathdata=pathdata):
	t=time.time()
	with open(pathdata+rpath,'r') as f:
		rdic=cPickle.load(f)
	print 'pickle load done in:{0} s'.format(time.time()-t)
	return rdic

