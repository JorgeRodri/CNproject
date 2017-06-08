'''
Created on 7 jun. 2017

@author: jorge
'''
from functions.Utils import clean_graph,load
from functions.Centrality import between_parallel
import networkx as nx
import matplotlib.pyplot as plt
import pickle 
import time



if __name__=='__main__':
    save_path='centrality/'
    #small graph
    G =nx.Graph(load('Networks/final_cleared.net'))
    print 'Starting...'
    #centrality by degree
    t1=time.time()
    degree_cent=nx.degree_centrality(G)
    with open(save_path+'degree_centrality.txt','wb') as f:
        pickle.dump(degree_cent, f)    
    t2=time.time()
    print('Degree centrality done, in time:'+str(t2-t1))
    
    
    eigen_cent=nx.eigenvector_centrality(G, max_iter=100, tol=1e-06) #tol is use to check corvengence
    with open(save_path+'eigenvector_centrality.txt','wb') as f:
        pickle.dump(eigen_cent, f)
    t1=time.time()
    print('Eigen vector centrality done, in time:'+str(t1-t2))
    
    closeness=nx.closeness_centrality(G)
    with open(save_path+'closeness_centrality.txt','wb') as f:
        pickle.dump(closeness, f)
    t2=time.time()
    print('Closeness centrality done, in time:'+str(t2-t1))
    
    betw_cent=nx.betweenness_centrality(G,k=None) # k can be to aproximate centrality, the highest the more accurate and costly
    with open(save_path+'betweenness_centrality.txt','wb') as f:
        pickle.dump(betw_cent, f)
    t1=time.time()
    print('Betweenness centrality done, in time:'+str(t1-t2))
    
    
    
    print 'getting betweenness by parallel pooling'
    t1=time.time()
    bt = between_parallel(G,4)
    with open(save_path+'betweenness_centrality_parallel_pooling.txt','wb') as f:
        pickle.dump(betw_cent, f)
    t2=time.time()
    print('Betweenness centrality done, in time:'+str(t2-t1))
    
    '''
    top=10
    print 'Preparing for plotting'
    spring_pos = nx.spring_layout(G)
    
    max_nodes =  sorted(bt.iteritems(), key = lambda v: -v[1])[:top]
    bt_values = [5]*len(G.nodes())
    bt_colors = [1]*len(G.nodes())
    print max_nodes
    for max_key, max_val in max_nodes:
        bt_values[G.nodes().index(max_key)] = 150
        bt_colors[G.nodes().index(max_key)] = 2
    
    plt.axis("off")
    nx.draw_networkx(G, pos = spring_pos, cmap = plt.get_cmap("rainbow"), node_color = bt_colors, node_size = bt_values, with_labels = False)
    plt.show()'''