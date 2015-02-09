#! -*- coding:utf-8 -*- 

from reco_tools import *
import random
import pylab


log=LogisticRegression()
clf=ExtraTreesClassifier(bootstrap=True,oob_score=True,n_estimators=5000)
clr=ExtraTreesRegressor(bootstrap=True,oob_score=True,n_estimators=5000)


rdic=load_rdic(rpath='ref_rubric_v2')
rdic[0]={'slug':'void'}

#print rdic

def main():
	
	analdic=load_rdic('vensam_d100_v2')
	click=analdic['clicked']
	appear=analdic['appear']
	
	analdic2=load_rdic('dimlun_d100_v2')
	#click2=analdic2['clicked']
	#appear2=analdic2['appear']
	
	#analdic=load_rdic('testtimeint')
	print analdic.keys()
	analdic['inner']=filter(lambda x:x!=None and 0<x <10000,analdic['inner'])
	analdic['outer']=filter(lambda x:x!=None and 0<x <10000,analdic['outer'])
	print len(analdic['inner'])
	print len(analdic['outer'])
	
	X=sp.array([analdic['inner']+analdic['outer']]).T
	
	pylab.subplot(2,2,1)
	pylab.boxplot(sp.array(analdic['inner']))
	pylab.title('samedi (en heures)')
	pylab.subplot(2,2,2)
	pylab.boxplot(sp.array(analdic['outer']))
	pylab.title('semaine (en heures)')
	pylab.subplot(2,2,3)
	pylab.boxplot(sp.array(analdic['inner'])/24)
	pylab.title('samedi (en jours)')
	pylab.subplot(2,2,4)
	pylab.boxplot(sp.array(analdic['outer'])/24)
	pylab.title('semaine (en jours)')
	pylab.show()
	raw_input()
	
	print random.sample(X,1000)
	Y=sp.zeros(len(analdic['inner'])+len(analdic['outer']))
	Y[:len(analdic['inner'])]=1
	#Y= Y[len(analdic['inner'])-10:len(analdic['inner'])+10]
	#X= X[len(analdic['inner'])-5:len(analdic['inner'])+10]
	#return
	coef,pvalue= GLMreg(Y,X,namelist=['time'],return_coefs=True)
	GLMreg(Y,X,namelist=['time'],return_coefs=False)

	print sp.exp(coef),pvalue
	return
	#compare_two_distrib(inner,outer)
	

	
def compare_two_distrib(click,appear,seuil=0.05,userdic=True):
	
	print 'nb clés distrib1:',len(click)
	clicktot=sum(click.values())
	print 'nb activités distrib1:',clicktot
	print 'nb clés distrib2:',len(appear)
	appeartot=sum(appear.values())
	print 'nb activités distrib2:',appeartot
	misskey=set(appear.keys()).difference(click.keys())
	
	print 'nombre de clees manquante dans distrib2:',len(misskey)
	if userdic:print 'clee manquante dans distrib1:',map(lambda x:rdic[x]['slug'],misskey)
	
	misskey2=set(click.keys()).difference(appear.keys())
	
	print 'nombre de clees manquante dans distrib1:',len(misskey2)
	if userdic:print 'clee manquante dans distrib2:',map(lambda x:rdic[x]['slug'],misskey2)
	
	res_list=[]
	setkey=set(click.keys()).intersection(appear.keys())
	lensetkey=len(setkey)
	i=0
	for key in setkey:
		#break
		i+=1
		Y=sp.zeros(clicktot+appeartot)
		Y[:clicktot]=1
		X=sp.zeros((clicktot+appeartot,1))
		X[:click[key]]=1
		X[clicktot:clicktot+appear[key]]=1
		try:
			if userdic:coefs,pvalues=GLMreg(Y,X,namelist=[rdic[key]['slug']],return_coefs=True)
			else:coefs,pvalues=GLMreg(Y,X,namelist=[key],return_coefs=True)
			
		except Exception as e:raise e
		
		if pvalues[1]<seuil:
			if userdic:res_list.append((rdic[key]['slug'],round(sp.exp(coefs[1]),3),round(pvalues[1],5)))
			else:res_list.append((key,round(sp.exp(coefs[1]),3),round(pvalues[1],5)))
		
		sys.stdout.write('\r {0} test done ({1} %)'.format(i,round(float(i)/lensetkey*100.0,2)))
		sys.stdout.flush()
		
	print ''
	res_list.sort(key=lambda x:x[1],reverse=True)
	
	for r in res_list:print r[0],r[1]
	
	i=0
	print '\n computing missing values:\n'
	res_list2=[]
	lensetkey2=len(set(click.keys()).union(appear.keys()).difference(setkey))
	for key in set(click.keys()).union(appear.keys()).difference(setkey):
		#break
		i+=1
		Y=sp.zeros(clicktot+appeartot)
		Y[:clicktot]=1
		X=sp.zeros((clicktot+appeartot,1))
		if key in click:X[:click[key]]=1
		if key in appear:X[clicktot:clicktot+appear[key]]=1
		
		Y=sp.array(list(Y)+[0,1])
		X=sp.vstack([X,[1],[1]])
		
		try:
			if userdic:coefs,pvalues=GLMreg(Y,X,namelist=[rdic[key]['slug']],return_coefs=True)
			else:coefs,pvalues=GLMreg(Y,X,namelist=[key],return_coefs=True)

		except Exception as e:raise e
		if pvalues[1]<seuil:
			
			if userdic:res_list2.append((rdic[key]['slug'],round(sp.exp(coefs[1]),3),round(pvalues[1],5)))
			else:res_list2.append((key,round(sp.exp(coefs[1]),3),round(pvalues[1],5)))
		
		sys.stdout.write('\r {0} test done ({1} %)'.format(i,round(float(i)/lensetkey2*100.0,2)))
		sys.stdout.flush()
		
	print ''
	res_list2.sort(key=lambda x:x[1],reverse=True)
	for r in res_list2:print r[0],r[1]
		
	pass





if __name__=='__main__':
	main()