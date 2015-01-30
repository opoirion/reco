#! -*- coding:utf-8 -*- 

import entities
from entities.mongo.source import Source
from entities.mongo.activity import Activity as MongoActivity
from entities.mysql.rubric import Rubric
from entities.mysql.connection import RawDataSessionManager as RawDataSession
import cPickle,sys,time
from entities.mysql._models import AddressTree
from entities.mysql.connection import RawDataSession as RDS
from elasticsearch import Elasticsearch
import copy
import scipy as sp
from scipy.spatial import distance
import datetime
from datection.export import schedule_to_discretised_days
import cPickle
import sys
import request
import extract_func
#sys.path.append('/home/oliver/Documents/clustering/scriptpython/')
#from clustering_tools import *



###################### Databases  #######################
session=RDS()
es=Elasticsearch(['http://chewbacca.mapado.com:9200/'])
#########################################################


pathdata='/home/oliver/Documents/reco/data/'

###################### Parameter  #######################
size=10000
#########################################################

pathdata='home/oliver/Documents/clustering/data/'
mongodicname='all_act_v2'

params={}

def main():
    #cl=take_data_BASE(size,fname='bleddata')
    #cl.change_request(request.request5,field='_source')
    #cl.process()
    #cl.save()
    
    load_query_click_data_raw(size,index='user_log',request=request.request4,func=extract_func.extract_score_multipass,params=params)
    #cl=take_data_BASE(daylist=['vendredi','samedi'],nbday=200)
    #cl.alter_request()
    #cl.alter_request_onlyclick()
    #cl.process()
    #cl.save()

    #cl3=take_data_v2(daylist=['samedi'],fname='testtimeint')
    #cl3.process()
    #cl3.save()
    return
	
	
	
	
def test():
	obj=MongoActivity.objects(id="541385fbea9ee71ebe60e64e").no_cache()
	#print obj[0].title, obj[0].front_address.latitude,obj[0].front_address.longitude
	#print obj[0].first_date
	#help(obj[0].schedule)
	schedule_discretised_days = schedule_to_discretised_days(obj[0].schedule)
	print schedule_discretised_days,len(schedule_discretised_days)
	res=session.query(AddressTree).filter(AddressTree.slug=='auray')
	#print res
	return


class take_data_BASE():
    def __init__(self,size=size,uptime=None,daylist=['vendredi','samedi'],fname=None,version='v2',nbday=200):
        self.fname=fname
        self.size=size
        self.nbday=nbday
        self.uptime=uptime
        self.version=version
        self.daylist=daylist
        self.mapday={'lundi':0,'mardi':1,'mercredi':2,'jeudi':3,'vendredi':4,'samedi':5,'dimanche':6}
        self.daylistint=[self.mapday[day] for day in self.daylist]
        self.request=request.request_BASE

    def change_request(self,request,field='fields'):
        self.field=field
        self.request=request
    def alter_request_onlyclick(self):
        self.request["filter"]["bool"]["must"][0]["terms"]["message"]=["clicked"]
    def alter_request(self):
        today=datetime.date.today()
        daylist=filter(lambda x:x.weekday() in self.daylistint,[today-datetime.timedelta(days=x) for x in range(self.nbday)])
        boollist={"should":[]}
        for day in daylist:
            boollist['should'].append({
                    "range":
                        {
                        "@timestamp":{
                            "gte":day.__str__(),
                            "lt":(day+datetime.timedelta(days=1)).__str__()
                            }
                        }
                    }
            )
        self.request["filter"]["bool"]["must"].append({"bool":boollist})


    def process(self):
        self.raw_list=self.load_query_click_data()
        self.process_rawlist()

    def save(self,path='../data/'):
        if not self.fname:
            self.fname=''
            for day in self.daylist:self.fname+=day[:3]
            self.fname+='_d{0}_{1}'.format(self.nbday,self.version)
            
        with open(path+self.fname,'w') as f:
            cPickle.dump(self.dic,f)
            
    def process_rawlist(self):
        self.dic={}
        for r in self.raw_list:
            
            if type(r['message'])!=list:r['message']=[r['message']]
            if type(r['ctxt_rubric.id'])!=list:r['ctxt_rubric.id']=[r['ctxt_rubric.id']]
            self.dic.setdefault(r["message"][0],{})
            self.dic[r["message"][0]].setdefault(r["ctxt_rubric.id"][0],0)
            self.dic[r["message"][0]][r["ctxt_rubric.id"][0]]+=1
            #print self.dic
        

    def load_query_click_data(self):
        
        res=es.search(index='user_log',body=self.request,size=self.size)['hits']['hits']
        
        raw_list=[]
        started=False
        i=0
        lenres=len(res)
        for r in res:
            i+=1
            if type(r[self.field]['@timestamp'])!=list:r[self.field]['@timestamp']=[r[self.field]['@timestamp']]
            #raw_input(r[self.field]['@timestamp'])
            d1=datetime.datetime(*map(lambda x:int(x.split('.')[0]),r[self.field]['@timestamp'][0].split('T',1)[0].split('-')+r[self.field]['@timestamp'][0].split('T',1)[1].strip('Z').split(':')))
            if not started:
                firstdate=d1
                started=True
            if "ctxt_rubric.id" not in r[self.field]:continue
            
            if (d1.weekday() in self.daylistint) and (not self.uptime or self.uptime<d1.time()):
                raw_list.append(copy.deepcopy(r[self.field]))
            sys.stdout.write('\r {0} request done ({1} %)'.format(i,round(float(i)/lenres*100.0,2)))
            sys.stdout.flush()
        lastdate=d1
        
        print ''
        print 'nombre de requete:',len(raw_list)
        print 'premiere date',firstdate
        print 'derniere date',lastdate
        print 'nombre de jours ecoulées:',(firstdate-lastdate).days
                
        return raw_list

	



class take_data_v1(take_data_BASE):
	def __init__(self,size=size,fname='../data/data_saved_v2_s100000',version='v1',daylist=[],nbday=200):
		take_data_BASE.__init__(self,size=size,fname=fname,version=version,daylist=daylist,nbday=nbday)
		
	def process(self):
		bindlist=load_query_click_data(size)
		print 'len bindlist:',len(bindlist)
		self.position=map(lambda x:x[1]['fields']['ctxt_activity.position'][0],bindlist)
		self.spatial_diff,mongodict=self.return_spatial_coordinate(bindlist)
		self.time_diff,self.duration_diff=self.return_days_interval(bindlist,mongodict)
		self.occurence=self.return_occurence(bindlist,mongodict)
	
	def save(self):
		with open(fname,'w') as f:
			cPickle.dump([self.duration_diff,self.occurence,self.time_diff,self.spatial_diff,self.position],f)

	def return_occurence(self,bindlist,mongodict):
		occurence=[]
		for bind in bindlist:
			nboccur=len(schedule_to_discretised_days(mongodict[bind[1]['fields']['activity.id'][0]].schedule))
			#print nboccur,bind[1]['fields']['activity.id'][0]
			occurence.append(nboccur)
			#raw_input()
		return occurence
	def return_spatial_coordinate(self,bindlist,mongodict=[],create_mongodict=True):
		coordinates_ref=[]
		coordinates_act=[]
		dist=[]
		i=0
		lenbind=len(bindlist)
		for bind in bindlist:
			i+=1
			if create_mongodict:
				bind1=MongoActivity.objects(id=bind[1]['fields']['activity.id'][0]).no_cache().limit(1).first()
			else:
				bind1=mongodict[bind[1]['fields']['activity.id'][0]]
				print bind1
			
			bind0=session.query(AddressTree).filter(AddressTree.slug==bind[0]['fields']['ctxt_addressTree'][0]).one()
			if create_mongodict:mongodict.append(bind1)
			try:
				coordinates_ref.append([bind0.latitude,bind0.longitude])
				coordinates_act.append([bind1.front_address.latitude,bind1.front_address.longitude])
				dist.append(distance.pdist([[bind0.latitude,bind0.longitude],[bind1.front_address.latitude,bind1.front_address.longitude]])[0])
			except Exception:continue
			sys.stdout.write('\r {0} request done ({1} %)'.format(i,round(float(i)/lenbind*100.0,2)))
			sys.stdout.flush()
		if create_mongodict:
			mongodict={str(mongo.id):mongo for mongo in mongodict}
			return dist,mongodict
		return dist
			
			
	def return_days_interval(self,bindlist,mongodict):
		time_diff=[]
		duration_diff=[]
		for bind in bindlist:
			
			d1=datetime.datetime(*map(lambda x:int(x),bind[0]['fields']['@timestamp'][0].split('T',1)[0].split('-')))
			d_first=mongodict[bind[1]['fields']['activity.id'][0]].first_date
			d_last=mongodict[bind[1]['fields']['activity.id'][0]].last_date
			if d_last and d_first and d_first<d1<d_last:
				time_diff.append(0)
				duration_diff.append((d_last-d1).days)
			elif d_last and d1>d_last:
				print "warning! date d'activité dépassé!"
				time_diff.append(None)
				duration_diff.append(None)
			else:
				if d_first:
					time_diff.append((d_first-d1).days)
					if not d_last:duration_diff.append(None)
					else:duration_diff.append((d_last-d_first).days)
				else:
					duration_diff.append(None)
					time_diff.append(None)
			#print duration_diff,bind[1]['fields']['activity.id'][0],d_first,d_last
			#raw_input()
		return time_diff,duration_diff
					
			
class take_data_v2(take_data_v1):
	def __init__(self,fname=None,daylist=['samedi'],version='v3',nbday=200):
		take_data_v1.__init__(self,daylist=daylist,version=version,nbday=nbday,fname=fname)
		
	def process(self):
		self.bindlist=load_query_click_data(size=self.size)
		self.process_rawlist()
		self.spatial_diff,mongodict=self.return_spatial_coordinate(self.bindlist)
		self.dic['inner'],_=return_time_interval(self.dic['inner'],mongodict)
		self.dic['outer'],_=return_time_interval(self.dic['outer'],mongodict)
		
		
	def process_rawlist(self):
		self.dic={'inner':[],'outer':[]}
		for bind in self.bindlist:
			bindsplit1=bind[1]['fields']['@timestamp'][0].split('T',1)
			d1=datetime.datetime(*map(lambda x:int(x.split('.')[0]),bindsplit1[0].split('-')+bindsplit1[1].strip('Z').split(':')))
			if d1.weekday() in self.daylistint:self.dic['inner'].append(bind)
			else:self.dic['outer'].append(bind)
			
	def save(self,path='../data/'):
		if not self.fname:
			self.fname=''
			for day in self.daylist:self.fname+=day[:3]
			self.fname+='_d{0}_{1}'.format(self.nbday,self.version)
			
		with open(path+self.fname,'w') as f:
			cPickle.dump(self.dic,f)

def load_query_click_data(size):
	
	request={ 
		"sort":[{"@timestamp":{"order":"desc"}}],
		"fields":["activity.id","message","user.token_key","ctxt_addressTree","@timestamp","ctxt_activity.position"],   
		"filter":{
			"bool": {
				"must": [ 
					{
						"terms":{
							"message":["activity_search","clicked"]
						}
					},
					{
						"term":{
							"user.seems_human": True
						}
					}
				]
			}
		}
		}
	
	res=es.search(index='user_log',body=request,size=size)['hits']['hits']
	
	usertoken=''
	currentrequest=None
	bindlist=[]
	clicked_dic={}
	
	for r in res:
		
		if r['fields']['message'][0]=='clicked':
			#print 'yeeeepe'
			try:
				assert(r['fields']['activity.id'])
				usertoken=r['fields']['user.token_key'][0]
				#print usertoken
				assert(r['fields']['ctxt_activity.position'])
			except Exception:
				continue
			else:clicked_dic[usertoken]=copy.deepcopy(r)
		elif r['fields']['message'][0]=='activity_search':
			try:
				assert(r['fields']['user.token_key'])
			except Exception:continue

			if r['fields']['user.token_key'][0] in clicked_dic:
				bindlist.append((copy.deepcopy(r),clicked_dic[r['fields']['user.token_key'][0]]))
		else:
			print 'something went wrong'
			raise(str(r)+str(r['fields']['message'][0]))
	return bindlist


def load_query_click_data_raw(size,index='activities',request=request.request,func=None,params={}):
	
	res=es.search(index=index,body=request,size=size,explain=True)
	
	if func:return func(res,**params)

		
			


def return_time_interval(bindlist,mongodict):
	time_diff=[]
	duration_diff=[]
	for bind in bindlist:
		bindsplit=bind[1]['fields']['@timestamp'][0].split('T',1)
		d1=datetime.datetime(*map(lambda x:int(x.split('.')[0]),bindsplit[0].split('-')+bindsplit[1].strip('Z').split(':')))
		#print '\nd1', d1
		d_first=mongodict[bind[1]['fields']['activity.id'][0]].first_date
		d_last=mongodict[bind[1]['fields']['activity.id'][0]].last_date
		#print 'dfirst',d_first
		#print 'last',d_last
		#print '\n'
		#sys.exit(1)
		if d_last and d_first and d_first<d1<d_last:
			time_diff.append((d_last-d1).total_seconds()/3600)
			duration_diff.append((d_last-d1).total_seconds()/3600)
		elif d_last and d1>d_last:
			print "warning! date d'activité dépassé!"
			time_diff.append(None)
			duration_diff.append(None)
		else:
			if d_first:
				time_diff.append((d_first-d1).total_seconds()/3600)
				if not d_last:duration_diff.append(None)
				else:duration_diff.append((d_last-d_first).total_seconds()/3600)
			else:
				duration_diff.append(None)
				time_diff.append(None)
		#print duration_diff,bind[1]['fields']['activity.id'][0],d_first,d_last
		#raw_input()
	return time_diff,duration_diff
			
			
	
if __name__=='__main__':
	main()
