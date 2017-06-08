'''
Created on 8 jun. 2017

@author: jorge
'''

from functions.Utils import load
from functions.Centrality import between_parallel
import networkx as nx
import pickle 
import time

#22937.9590001s time, no parallel and implemnted function in Nx 57334.8970001

if __name__=='__main__':
    save_path='centrality/'
    #small graph
    G =nx.Graph(load('Networks/final_cleared.net'))
    print 'Starting...'
    print 'Getting betweenness by parallel pooling in 4 pools.'
    t1=time.time()
    bt = between_parallel(G,4)
    with open(save_path+'betweenness_centrality_parallel_pooling2.txt','wb') as f:
        pickle.dump(bt, f)
    t2=time.time()
    print('Betweenness centrality done, in time:'+str(t2-t1))