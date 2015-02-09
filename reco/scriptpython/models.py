import datetime
import request_tools

querydic_basic ={ 
            'factor' :{
                'image' : 4,
                'occurence': 3,
                'duration' : 2,
                'lat_lng':  3.5,
                'time-proximity' : 2,
                'rubric-on' : 1.5,
                'tags-on.label' : 1,
                'tags-on.categorie' : 1.5
            },
            'normfactor' : {
                'lat_lng':  {'mean' : 0.0, 'std' : 1},
                'time-proximity' : {'mean' : 0, 'std' : 1},
                'rubric-on' : {'mean' : 0.0, 'std' : 0.2},
                'tags-on.label' : {'mean' : 0.0, 'std' : 0.2},
                'tags-on.categorie' : {'mean' : 0.0, 'std' : 0.2}
            },
            'version' : 1,
            'name' : 'all big city',
            'generic':0,
            'days' : ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],
            'time': {
                    'begin' : '00:00',
                    'end' : '23:59'
            },
            'learningRate' : 0.1,
            'what': {}
        }
            
querydic_proximity ={ 
    
            'factor' :{
                'image' : 3,
                'occurence': 3,
                'duration' : 2,
                'lat_lng':  4.5,
                'time-proximity' : 2,
                'rubric-on' : 1.5,
                'tags-on.label' : 1.0,
                'tags-on.categorie' : 1.5
            },
            'normfactor' : {
                'lat_lng':  {'mean' : 0.0, 'std' : 1},
                'time-proximity' : {'mean' : 0, 'std' : 1},
                'rubric-on' : {'mean' : 0.0, 'std' : 0.2},
                'tags-on.label' : {'mean' : 0.0, 'std' : 0.2},
                'tags-on.categorie' : {'mean' : 0.0, 'std' : 0.2}
            },
            'version' : 1,
            'name' : 'generic (dumped with small town)',
            'generic':1,
            'days' : ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],
            'time': {
                    'begin' : '00:00',
                    'end' : '23:59'
            },
            'learningRate' : 0.1,
            'what': {}
        }
            
querydic_basic_we ={ 
            'factor' :{
                'image' : 3,
                'occurence': 3,
                'duration' : 2,
                'lat_lng':  3,
                'time-proximity' : 4.5,
                'rubric-on' : 1.5,
                'tags-on.label' : 1.0,
                'tags-on.categorie' : 1.5
            },
            'normfactor' : {
                'lat_lng':  {'mean' : 0.0, 'std' : 1},
                'time-proximity' : {'mean' : 0, 'std' : 1},
                'rubric-on' : {'mean' : 0.0, 'std' : 0.2},
                'tags-on.label' : {'mean' : 0.0, 'std' : 0.2},
                'tags-on.categorie' : {'mean' : 0.0, 'std' : 0.2}
            },
            'version' : 1,
            'name' : 'all big city week end',
            'generic':0,
            'days' : ['Fri','Sat'],
            'time': {
                    'begin' : '20:00',
                    'end' : '23:59'
            },
            'learningRate' : 0.2,
            'what': {}
        }
            

querydic_proximity_we ={ 
    
            'factor' :{
                'image' : 3,
                'occurence': 3,
                'duration' : 2,
                'lat_lng':  4.5,
                'time-proximity' : 4,
                'rubric-on' : 1.0,
                'tags-on.label' : 0.5,
                'tags-on.categorie' : 1
            },
            'normfactor' : {
                'lat_lng':  {'mean' : 0.0, 'std' : 1},
                'time-proximity' : {'mean' : 0, 'std' : 1},
                'rubric-on' : {'mean' : 0.0, 'std' : 0.2},
                'tags-on.label' : {'mean' : 0.0, 'std' : 0.2},
                'tags-on.categorie' : {'mean' : 0.0, 'std' : 0.2}
            },
            'version' : 1,
            'name' : 'generic week end (dumped with small town)',
            'generic':0,
            'days' : ['Fri','Sat'],
            'time': {
                    'begin' : '20:00',
                    'end' : '23:59'
            },
            'learningRate' : 0.2,
            'what': {}
            
        }
    
