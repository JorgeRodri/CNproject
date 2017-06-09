'''
Created on 8 jun. 2017

@author: jorge
'''

import networkx as nx
from functions.Utils import load, save, transform_into_dict, join_data, inverse_data
import time
import community
from collections import Counter

def aux(my_map):
    inv_map = {}
    for k, v in my_map.iteritems():
        inv_map[v] = inv_map.get(v, [])
        inv_map[v].append(k)
    return inv_map  

if __name__=='__main__':
    
    G=nx.Graph(load('Networks/final_cleared.net'))
    #join_data()
    #inverse_data()
    #transform_into_dict()
    data=load('Data/dict_data.txt')
    games_data=load('Data/inverse_data.txt')
    
    print('Load of files done. Calculating communities.')
    t1=time.time()
    part = community.best_partition(G)
    t2=time.time()
    
    print('Needed time for community detection: '+str(t2-t1))
    communities=set(part.values())
    print('number of communities='+str(len(communities)))
    comms = [part[node] for node in G.nodes()]
    members_in_communities=aux(part)
    print 'Creating a data dictionary.'
    #print members_in_communities
    #print part
    
    dict_comm={}
    n=0
    for comm in members_in_communities.keys():
        n+=1
        print n
        dict_comm[comm]=[0,[], []]
        for user in members_in_communities[comm]:
            dict_comm[comm]=[dict_comm[comm][0]+data[user][0], dict_comm[comm][1]+data[user][1], dict_comm[comm][2]+data[user][2]]
        dict_comm[comm]=[dict_comm[comm][0]/len(members_in_communities[comm]),Counter(dict_comm[comm][1]), Counter(dict_comm[comm][2])]
    print 'Saving the results'
    save(dict_comm, 'Data/Community_dict.txt')
    save(part,'Data/Communities.txt')
    
    
    
        
