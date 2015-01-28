request_BASE={ 
            "sort":[{"@timestamp":{"order":"desc"}}],
            "fields":["activity.id","message","ctxt_rubric.id","@timestamp","ctxt_activity.position"],   
            "filter":{
                "bool": {
                    "must": [ 
                        {
                            "terms":{
                                "message":["appear","clicked"]
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

request={
        "query": {

            "filtered": {
                "query": {
                    "function_score": {
                    "functions": [
                    {
                    "script_score": {
                        "script": "_score=0;def _i=1; for( key in tags_vector.keySet().intersect(doc['wiki_tags.tags'])){if(tags_vector[key]){_i+=1;};_score +=  factor * tags_vector[key]};return _score/_i;",
                        "params": {
                        "factor": 1,
                        "tags_vector": {
                        "atelier": 1,
                        "cirque": 1,
                        "comedien": 1
                        }
                        }
                    }
                    },
                    {
                    "script_score": {
                        "script": "_score=0;def _i=1; for( key in tags_vector.keySet().intersect(doc['wiki_tags.tags'])){if(tags_vector[key]){_i+=1;};_score +=  factor * tags_vector[key]};return _score/_i;",
                        "params": {
                        "factor": 1,
                        "tags_vector": {
                        "atelier": 1,
                        "cirque": 1,
                        "comedien": 1
                        }
                        }
                    }
                    }
                    ]
                    }
                },
                "filter": {
                        "exists": {
                            "field": "wiki_tags"
                        }
                    }
                }
            }
        }
request2={
  "sort": [
    {
      "@timestamp": {
        "order": "desc"
      }
    }
  ],
  "query": {
    "filtered": {
      "filter": {
        "and": {
          "filters": [
            {
              "exists": {
                "field": "ctxt_function_explanation"
              }
            },
            {
              "bool": {
                "must": [
                  {
                    "term": {
                      "message": "clicked"
                    }
                  },
                  {
                    "term": {
                      "ctxt_function_explanation.field_or_function": "lat_lng"
                    }
                  }
                ]
              }
            },
            {
              "not": {
                "filter": {"term": {
                  "ctxt_search.when": "today"
                }}
              }
            }
          ]
        }
      }
    }
  }
}
request3={
  "sort": [
    {
      "@timestamp": {
        "order": "desc"
      }
    }
  ],
  "query": {
    "filtered": {
      "filter": {
        "and": {
          "filters": [
            {
              "exists": {
                "field": "ctxt_function_explanation"
              }
            },
            {
              "bool": {
                "must": [
                  {
                    "term": {
                      "message": "appear"
                    }
                  },
                  {
                    "term": {
                      "ctxt_function_explanation.field_or_function": "lat_lng"
                    }
                  }
                ]
              }
            },
            {
              "not": {
                "filter": {"term": {
                  "ctxt_search.when": "today"
                }}
              }
            }
          ]
        }
      }
    }
  }
}
request4={
  "sort": [
    {
      "@timestamp": {
        "order": "desc"
      }
    }
  ],
  "query": {
    "filtered": {
      "filter": {
        "and": {
          "filters": [
            {
              "exists": {
                "field": "ctxt_function_explanation"
              }
            },
            {
              "bool": {
                "must": [
                  {
                    "terms": {
                      "message": [
                        "clicked","appear"
                      ]
                    }
                  },
                  {
                    "term": {
                      "ctxt_function_explanation.field_or_function": "lat_lng"
                    }
                  },
                  {
                     "terms": {
                      "ctxt_search.addressTree": ["paris","lyon","marseille","toulouse","bordeaux","nantes","grenoble","strasbourg"]
                    } 
                  }
                ]
              }
            },
            {
              "not": {
                "filter": {"term": {
                  "ctxt_search.when": "today"
                }}
              }
            }
          ]
        }
      }
    }
  }
}
request5={
  "sort": [
    {
      "@timestamp": {
        "order": "desc"
      }
    }
  ],
  "query": {
    "filtered": {
      "filter": {
        "and": {
          "filters": [
            {
              "exists": {
                "field": "ctxt_function_explanation"
              }
            },
            {
              "bool": {
                "must": [
                  {
                    "terms": {
                      "message": [
                        "clicked","appear"
                      ]
                    }
                  },
                  {
                    "term": {
                      "ctxt_function_explanation.field_or_function": "lat_lng"
                    }
                  },
                  {
                     "terms": {
                      "ctxt_search.addressTree": ["montrond-les-bains","loire-42","saint-just-saint-rambert","pau","tournon-sur-rhone"," aquitaine","wittenheim","montelimar","la-roche-sur-foron"]
                    } 
                  }
                ]
              }
            },
            {
              "not": {
                "filter": {"term": {
                  "ctxt_search.when": "today"
                }}
              }
            }
          ]
        }
      }
    }
  }
}   