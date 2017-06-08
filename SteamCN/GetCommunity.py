'''
Created on 8 jun. 2017

@author: jorge
'''

import networkx as nx
from functions.Utils import load, save
import time
import community

if __name__=='__main__':
    
    G=load('Networks/final_cleared.net')
    
    print('Starting...')
    #np.random.seed(51111)
        
    #pos=nx.spring_layout(H)
    
    #plt.axis('off')
    #nx.draw_networkx(H,pos,with_labels=False)
    
    
    t1=time.time()
    part = community.best_partition(H)
    t2=time.time()
    
    print('Needed time for community detection: '+str(t2-t1))
    values = [part.get(node) for node in H.nodes()]
        
    nx.draw_spring(H, 
                       cmap = plt.get_cmap('jet'),
                       node_color = values, 
                       #node_size=30, 
                       with_labels=False)
    
    plt.show()
    time.sleep(30)
    try:
        plt.close()
    except: 
        pass
    
    print('Doing it in a different way')
    # another way to obtain the same
    partition = part
    
    #drawing
    size = float(len(set(partition.values())))
    pos = nx.spring_layout(H)
    count = 0.
    for com in set(partition.values()) :
        count = count + 1.
        list_nodes = [nodes for nodes in partition.keys()
                                    if partition[nodes] == com]
        nx.draw_networkx_nodes(H, pos, list_nodes, node_size = 20,
                                    node_color = str(count / size))
    
    
    nx.draw_networkx_edges(H,pos, alpha=0.5)
    plt.show()

