curl -XXGET 'http://chewbacca.mapado.com:9200/user_log/_search?pretty=true&size=1' -d '{ 

"sort":["@timestamp","user.token_key"],
"fields":["@timestamp","message","ctxt_activity.position"],   
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
					"user.seems_human": true
				}
			}
		]
	}
}
}'