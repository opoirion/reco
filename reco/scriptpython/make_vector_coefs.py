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


###################### Databases  #######################
session=RDS()
es=Elasticsearch(['http://chewbacca.mapado.com:9200/'])
#########################################################


###################### Parameter  #######################
size=1000
#########################################################


def main():
        res=es.index(index='reco_models',doc_type="models",body={"python_test":"success",'idd':4})
        print res
        return
        req=request.request_aggregation_CITY
        res=es.search(index='user_log',body=req,size=size)
        RubricVector=process_agg_res_ratio(res,'rubric')
        SemCatVector=process_agg_res_ratio(res,'categorie',100)
        SemLabelVector=process_agg_res_ratio(res,'label',100)
        
        
        print SemLabelVector

        
def process_agg_res_ratio(res,field='rubric',threshold=None):
        resdic={}
        for r in res['aggregations'][field]['buckets']:
                resdic[r['key']]={bucket['key']:bucket['doc_count'] for bucket in r['message']['buckets']}
                if not resdic[r['key']].has_key('clicked'): resdic.pop(r['key'])
                elif not resdic[r['key']].has_key('appear'):resdic[r['key']]['appear']=1
        for key in resdic:
                resdic[key]=float(resdic[key]['clicked'])/resdic[key]['appear']
        if threshold:
                resdic={x[0]:x[1] for x in sorted(resdic.items(),key=lambda x:x[1])[:threshold]}
        m=max(resdic.values())
        for key in resdic:resdic[key]/=m
        return resdic

def process_agg_res_count(res,field='categorie',threshold=100):
        resdic={}
        for r in res['aggregations'][field]['buckets']:
                resdic[r['key']]={bucket['key']:bucket['doc_count'] for bucket in r['message']['buckets']}
                if not resdic[r['key']].has_key('clicked'): resdic.pop(r['key'])
                elif not resdic[r['key']].has_key('appear'):resdic[r['key']]['appear']=1

        for key in resdic:
                resdic[key]=float(resdic[key]['clicked'])
        if threshold:
                resdic={x[0]:x[1] for x in sorted(resdic.items(),key=lambda x:x[1])[:threshold]}
        m=max(resdic.values())

        for key in resdic:resdic[key]/=m
        return resdic

if __name__=='__main__':
        main()