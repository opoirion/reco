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
                     "terms": {
                      "ctxt_search.addressTree": ["paris","lyon","marseille","toulouse","bordeaux","nantes","grenoble","strasbourg","reims","montpellier","nice","toulon"]
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
                      "ctxt_search.addressTree": ["montrond-les-bains","loire-42","saint-just-saint-rambert","pau","tournon-sur-rhone"," aquitaine","wittenheim","montelimar","la-roche-sur-foron","bourg-en-bresse","aix-les-bains","annecy","fos-sur-mer","annemasse","bons-en-chablais","chambery"]
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
                
request_aggregation_CITY={
   "query": {
      "filtered": {
         "filter": {
            "bool": {
               "must": [
                  {
                     "terms": {
                        "ctxt_search.addressTree": ["paris","lyon","marseille","toulouse","bordeaux","nantes","grenoble","strasbourg"]
                     }
                  },
                  {
                     "term": {
                        "user.seems_human": True
                     }
                  },
                  {
                     "terms": {
                        "message": [
                           "appear",
                           "clicked"
                        ]
                     }
                  }
               ]
            }
         }
      }
   },
   "size": 0,
   "aggs": {
      "rubric": {
         "terms": {
            "field": "ctxt_rubric.id",
            "size": 0
         },
         "aggs": {
            "message": {
               "terms": {
                  "field": "message"
               }
            }
         }
      },
      "categorie": {
         "terms": {
            "field": "ctxt_sem_tags.categorie.name",
            "size": 0
         },
         "aggs": {
            "message": {
               "terms": {
                  "field": "message"
               }
            }
         }
      },
      "label": {
         "terms": {
            "field": "ctxt_sem_tags.label.name",
            "size": 0
         },
         "aggs": {
            "message": {
               "terms": {
                  "field": "message"
               }
            }
         }
      }
   }
}

request_aggregation_SMALL={
   "query": {
      "filtered": {
         "filter": {
            "bool": {
               "must": [
                  {
                     "terms": {
                        "ctxt_search.addressTree": ["montrond-les-bains","loire-42","saint-just-saint-rambert","pau","tournon-sur-rhone"," aquitaine","wittenheim","montelimar","la-roche-sur-foron","bourg-en-bresse","aix-les-bains","annecy","fos-sur-mer","annemasse","bons-en-chablais","chambery"]
                     }
                  },
                  {
                     "term": {
                        "user.seems_human": True
                     }
                  },
                  {
                     "terms": {
                        "message": [
                           "appear",
                           "clicked"
                        ]
                     }
                  }
               ]
            }
         }
      }
   },
   "size": 0,
   "aggs": {
      "rubric": {
         "terms": {
            "field": "ctxt_rubric.id",
            "size": 0
         },
         "aggs": {
            "message": {
               "terms": {
                  "field": "message"
               }
            }
         }
      },
      "categorie": {
         "terms": {
            "field": "ctxt_sem_tags.categorie.name",
            "size": 0
         },
         "aggs": {
            "message": {
               "terms": {
                  "field": "message"
               }
            }
         }
      },
      "label": {
         "terms": {
            "field": "ctxt_sem_tags.label.name",
            "size": 0
         },
         "aggs": {
            "message": {
               "terms": {
                  "field": "message"
               }
            }
         }
      }
   }
}
               
               
