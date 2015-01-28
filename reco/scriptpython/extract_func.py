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
    score={'clicked':{param:[] for param in params},'appear':{param:[] for param in params}}
    
        
    for r in res['hits']['hits']:
        
        message=r['_source']['message']
        r=r['_source']['ctxt_function_explanation']
        
        for param in params:
            try:
                score[message][param].append(filter(lambda x:x['field_or_function']==param,r)[0]['score'])
            except Exception as e:
                print '============>',e
                print r
                print param
                #raw_input()
    height=len(score['clicked'])
    pylab.figure(figsize=(14,18))
    i=1
    for field in params:
        if score['clicked'][field]:
            pylab.subplot(height,2,i)
            i+=1
            pylab.hist(score['clicked'][field],50,color='r')
            meanclick=sp.mean(score['clicked'][field])
            stdclick=sp.std(score['clicked'][field])
            pylab.xlabel('{0} clicked mean:{1} std:{2} l:{3}'.format(field,round(meanclick,2),round(stdclick,2),len(score['clicked'][field])))
        if score['appear'][field]:
            pylab.subplot(height,2,i)
            i+=1
            meanappear=sp.mean(score['appear'][field])
            stdappear=sp.std(score['appear'][field])
            pylab.hist(score['appear'][field],50,color='g')
            pylab.xlabel('{0} appear mean:{1} std:{2} l:{3}'.format(field,round(meanappear,2),round(stdappear,2),len(score['appear'][field])))
        print field
        print round(meanclick,2),round(meanappear,2)
        print round(stdclick,2),round(stdappear,2)
        print 'longeur: ',len(score['clicked'][field]),len(score['appear'][field])
    pylab.savefig('../img/distrib_all_bled.png')
    
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
    
    