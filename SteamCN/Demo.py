'''
Created on 22 may. 2017

@author: Ricard and Jorge
'''
from functions.Utils import save, load, join_data, inverse_data, transform_into_dict, clean_graph
from functions.generators import download_games
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from functions.Centrality import between_parallel
import time
import community
from collections import Counter
import pickle 

def takeSecond(elem):
    return elem[1]

def histogram(G, log=False, norm=False,cumu=0, n=10):
    degrees=G.degree().values()
    if log:
        plt.title("Log Histogram.")
        logbins = np.logspace(np.log10(min(degrees)), np.log10(max(degrees)), n)
        plt.hist(degrees, bins = logbins, cumulative=cumu, normed=norm)
        plt.gca().set_xscale('log')
        plt.gca().set_yscale('log')
        #plt.show()
    else:  
        plt.hist(degrees, n,cumulative=cumu, normed=norm)  # plt.hist passes it's arguments to np.histogram
        plt.title("Histogram without log.")
        #plt.show()
    return plt


name_network='demo.net' # there are other 2 networks that can be used: final_uncleared and demo2 but they are larger

if __name__=='__main__':
    path='Networks/'
    G=load(path+name_network)
    G=nx.Graph(clean_graph(G))
    data=load('Data/dict_data.txt')
    games_data=load('Data/inverse_data.txt')
    
    
    print 'Data loaded'
    
    print 'Most Played Games:'

    x=[(i,games_data[i][1], games_data[i][0]) for i in games_data.keys()]
    
    
    sorted_x = sorted(x, reverse=True, key=takeSecond)
    
    print sorted_x[0:13]
    
    spring_pos = nx.spring_layout(G)
    print 'General information of the graph.'
    
    
    H=nx.Graph(G)
    
    print(nx.info(H))
    
            
    numbNodes=H.number_of_nodes()
    numbEdges=H.number_of_edges()
            
    print('Number of nodes: ' + str(numbNodes))
    print('Number of edges: ' + str(numbEdges))
    
    degrees=nx.degree(H).values()
            
    print('Degree in formation: ' + 'Mean: ' + str(np.mean(degrees)) + ', Maximum: '+ str(max(degrees))  +' and Minimum: '+ str(min(degrees)))
            
    clustering=nx.clustering(nx.Graph(H)).values()
    print('Average clustering coefficient: ' + str(np.mean(clustering)))
            
    assortativity=nx.degree_assortativity_coefficient(H)        
    print('Assortativity: '+str(assortativity))
         
    average_path = nx.average_shortest_path_length(H)
    diameter=nx.diameter(H)
    print('Average path length: '+str(average_path)+ '\nDiameter: '+str(diameter))
            
    
    #partition = community.best_partition(H)
    
    plt1=histogram(H, log=False, norm=True,cumu=0, n=10)
    plt1.xlabel('Relative frequencies')
    plt1.ylabel('Degree of the node')
    plt1.title('Histogram in the usual scale')
    plt1.show()
    
    plt2=histogram(H, log=True, norm=True,cumu=0, n=10)
    plt2.xlabel('Log frequencies')
    plt2.ylabel('Log scale degree')
    plt2.title('Histogram in Log scale')
    plt2.show()
    
    
    ### community detection by louvain
    ##### Comumunity detection
    
    
    
    print('Load of files done. Calculating communities.')
    t1=time.time()
    part = community.best_partition(G)
    t2=time.time()
    
    print('Needed time for community detection: '+str(t2-t1))
    communities=set(part.values())
    print('number of communities='+str(len(communities)))
    
    values = [part.get(node) for node in G.nodes()]

    plt.axis("off")
    nx.draw_networkx(G, pos = spring_pos, cmap = plt.get_cmap("jet"), node_color = values, node_size = 35, with_labels = False)
    plt.show()

    
    ##
    ## CENTRALITY
    ##
    #degree centrality
    bt=nx.degree_centrality(G)
    
    top = 10
    
    max_nodes =  sorted(bt.iteritems(), key = lambda v: -v[1])[:top]
    bt_values = [70]*len(G.nodes())
    bt_colors = [0]*len(G.nodes())
    for max_key, max_val in max_nodes:
        bt_values[G.nodes().index(max_key)] = 300
        bt_colors[G.nodes().index(max_key)] = 2
     
    plt.axis("off")
    nx.draw_networkx(G, pos = spring_pos, cmap = plt.get_cmap("rainbow"), node_color = bt_colors, node_size = bt_values, with_labels = False)
    plt.show()
    
    #eigen centrality
    """bt=nx.eigenvector_centrality(G, max_iter=100, tol=1e-06) #tol is use to check corvengence
    
    max_nodes =  sorted(bt.iteritems(), key = lambda v: -v[1])[:top]
    bt_values = [5]*len(G.nodes())
    bt_colors = [0]*len(G.nodes())
    for max_key, max_val in max_nodes:
        bt_values[G.nodes().index(max_key)] = 150
        bt_colors[G.nodes().index(max_key)] = 2
     
    plt.axis("off")
    nx.draw_networkx(G, pos = spring_pos, cmap = plt.get_cmap("rainbow"), node_color = bt_colors, node_size = bt_values, with_labels = False)
    plt.show()"""
    
    #closeness centrality
    closeness=nx.closeness_centrality(G)
    
    max_nodes =  sorted(bt.iteritems(), key = lambda v: -v[1])[:top]
    bt_values = [70]*len(G.nodes())
    bt_colors = [0]*len(G.nodes())
    for max_key, max_val in max_nodes:
        bt_values[G.nodes().index(max_key)] = 300
        bt_colors[G.nodes().index(max_key)] = 2
     
    plt.axis("off")
    nx.draw_networkx(G, pos = spring_pos, cmap = plt.get_cmap("rainbow"), node_color = bt_colors, node_size = bt_values, with_labels = False)
    plt.show()
    
    #betweenness centrality
    bt = between_parallel(G,4)
    
    max_nodes =  sorted(bt.iteritems(), key = lambda v: -v[1])[:top]
    bt_values = [70]*len(G.nodes())
    bt_colors = [0]*len(G.nodes())
    for max_key, max_val in max_nodes:
        bt_values[G.nodes().index(max_key)] = 300
        bt_colors[G.nodes().index(max_key)] = 2
     
    plt.axis("off")
    nx.draw_networkx(G, pos = spring_pos, cmap = plt.get_cmap("rainbow"), node_color = bt_colors, node_size = bt_values, with_labels = False)
    plt.show()