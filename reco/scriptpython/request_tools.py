import datetime
mapday={"Mon":0,"Tue":1,"Wed":2,"Thu":3,"Fri":4,"Sat":5,"Sun":6}
time_example={"begin":"20:00","end":"23:59"}

def alter_request(request,daylist,nbday=100,time={"begin":None,"end":None}):
    daylistint = [mapday[day] for day in daylist]
    today=datetime.date.today()
    today=datetime.datetime(today.year,today.month,today.day)
    
    if time["begin"]:
        hb,mb=map(lambda x:float(x),time["begin"].split(":"))
        delta_begin = datetime.timedelta( hb / 24 + mb / 1440  )
    if time["end"]:
        he,me=map(lambda x:float(x),time["end"].split(":"))
        delta_end = datetime.timedelta( he / 24 + me / 1440  )

        
    daylist=filter(lambda x:x.weekday() in daylistint,[today-datetime.timedelta(days=x) for x in range(nbday)])
    boollist={"should":[]}
    for day in daylist:
        if time["begin"]:gte = "{0}T{1}Z".format((day + delta_begin ).date().__str__(),(day + delta_begin ).time().__str__())
        else :gte= day.__str__()
        if time["end"]:lt =  "{0}T{1}Z".format((day + delta_end ).date().__str__(),(day + delta_end ).time().__str__())
        else :lt = (day+datetime.timedelta(days=1)).__str__()
            
        boollist["should"].append({
                "range":
                    {
                    "@timestamp":{
                        "gte": gte,
                        "lt": lt
                        }
                    }
                }
        )
    request["query"]["filtered"]["filter"]["bool"]["must"].append({"bool":boollist})
    
    
def main():
    import request
    import json
    alter_request(request.request_aggregation_CITY,["lundi","mardi"],nbday=100,time=time_example) 
    print json.dumps(request.request_aggregation_CITY)
    
if __name__ == "__main__":
    main()