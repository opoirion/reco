querydic_basic ={ 
            'factor' :{
                'image' : 4,
                'occurence': 3,
                'duration' : 2,
                'lat_lng':  3,
                'time-proximity' : 4,
                'rubric-on' : 1.0,
                'tags-on.label' : 0.5,
                'tags-on.categorie' : 1.0
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
            'generic':False
        }
            
querydic_proximity ={ 
            'factor' :{
                'image' : 3,
                'occurence': 3,
                'duration' : 2,
                'lat_lng':  4.5,
                'time-proximity' : 4,
                'rubric-on' : 0.5,
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
            'name' : 'generic (dumped with small town)',
            'generic':True
        }