import scipy as sp
import pylab

def extract_score(res,**params):
    score={param:[] for param in params}
    print score
    
    for r in res['hits']['hits']:
        #raw_input(r['_source']['ctxt_function_explanation'])
        r=r['_source']['ctxt_function_explanation']
        for param in score:
            try:
                score[param].append(filter(lambda x:x['field_or_function']==param,r)[0]['score'])
            except Exception:
                print r
                print param
                #raw_input()
    height=round(float(len(score))/2)
    pylab.figure(figsize=(12,12))
    i=1
    for field in score:
        pylab.subplot(height,2,i)
        i+=1
        pylab.hist(score[field],50)
        pylab.xlabel(field)
        print field
        print sp.mean(score[field])
        print sp.std(score[field])
    pylab.savefig('distrib_clicked.png')
    
    return score


def extract_score_multipass(res,**params):
    score={'clicked':{},'appear':{}}

    
        
    for r in res['hits']['hits']:
        
        message=r['_source']['message']
        r=r['_source']['ctxt_function_explanation']
       
        for bucket in r:
                key=bucket['field_or_function']
                if not score[message].has_key(key):score[message][key]=[]
                score[message][key].append(bucket['score'])
                
                
    height=max([len(score['clicked']),len(score['appear'])])
    pylab.figure(figsize=(14,30))
    i=1
    for field in set(score['clicked'].keys()+score['appear'].keys()):
        if score['clicked'].has_key(field):
           
            pylab.subplot(height,2,i)
            i+=1
            try:
                pylab.hist(score['clicked'][field],50,color='r')
            except Exception:
                print 'err with:',field
                pylab.text(0.5,0.5,'problem with {0}'.format(field))
                
            meanclick=sp.mean(score['clicked'][field])
            stdclick=sp.std(score['clicked'][field])
            pylab.xlabel('{0} clicked mean:{1} std:{2} l:{3}'.format(field,round(meanclick,2),round(stdclick,2),len(score['clicked'][field])))
        if score['appear'].has_key(field):
            pylab.subplot(height,2,i)
            i+=1
            meanappear=sp.mean(score['appear'][field])
            stdappear=sp.std(score['appear'][field])
            try:
                pylab.hist(score['appear'][field],50,color='g')
            except Exception:
                print 'err with:',field
                pylab.text(0.5,0.5,'problem with {0}'.format(field))
            pylab.xlabel('{0} appear mean:{1} std:{2} l:{3}'.format(field,round(meanappear,2),round(stdappear,2),len(score['appear'][field])))
        print field
        print round(meanclick,4),round(meanappear,4)
        print round(stdclick,4),round(stdappear,4)
        print 'longeur: ',len(score['clicked'][field]),len(score['appear'][field])
    pylab.savefig('../img/{0}'.format(params['figname']))
    
    return score


def anal_score(res,**params):
    
    for r in res['hits']['hits']:
        #raw_input(r['_source']['ctxt_function_explanation'])
        rr=r['_source']['ctxt_function_explanation']
        
        try:
            if filter(lambda x:x['field_or_function']=='time-proximity',rr)[0]['score']==1:
                print r
                print rr
                raw_input()
        except Exception:
            print 'eeer',r
            #raw_input()
    return score
    
    