#!/usr/bin/env python
# encoding: utf-8
'''
functions.Utils -- shortdesc

functions.Utils is a description

It defines classes_and_methods

@author:     user_name

@copyright:  2017 organization_name. All rights reserved.

@license:    license

@contact:    user_email
@deffield    updated: Updated
'''
import pickle
import networkx as nx
from os import listdir, remove
from os.path import isfile, join

def clean_graph(G, degree=1, method='Size', reached=None):
    H=G.copy()
    if method=='Size':
        degrees=H.degree()
        for i in H.nodes():
            if degrees[i]<=degree:
                H.remove_node(i)
    elif method=='Done' and reached!=None:
        nodes=H.nodes()
        for node in reached:
            if node not in nodes:
                H.remove_node(i)
    elif method=='Done' and reached==None:
        raise NameError('Wrong values, for this method a reached list of nodes is require')
    else:
        raise NameError('Wrong Method, try: Size or Size')
    return H

def save(data, name):
    try:
        nx.write_pajek(data,name)
    except:
        with open(name, 'wb') as f:
            pickle.dump(data, f)

def load(name):
    if name[-4:]=='.net':
        G=nx.read_pajek(name)
    else:
        try: 
            with open(name, 'rb') as f:
                G = pickle.load(f)
        except:
            raise('Wrong file')
    return G

def join_data():
    namefiles = [f for f in listdir('Data/') if isfile(join('Data/', f))]
    
    j_data = []
    for name in namefiles:
        if "data" in name:
            data=load('Data/'+name)
            for d in data:
                if d not in j_data:
                    j_data.append(d)
            remove(join('Data/', name))
    save(j_data, 'Data/final_data.txt')
                    
    