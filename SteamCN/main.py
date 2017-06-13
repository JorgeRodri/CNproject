'''
Created on 22 may. 2017

@author: Ricard and Jorge
'''
from functions.Utils import save, load, join_data, inverse_data, transform_into_dict, clean_graph
from functions.generators import download_games
import networkx as nx
import matplotlib.pyplot as plt
from functions.Centrality import between_parallel

name_network='demo.net'
if __name__=='__main__':
    path='Networks/'
    G=load(path+name_network)
    G=nx.Graph(clean_graph(G))
    

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
            
    data_results=( numbNodes, numbEdges, np.mean(degrees), max(degrees), min(degrees), np.mean(clustering), assortativity, average_path, diameter)
    save(data_results, save_path+'str_des.txt')
    
    #partition = community.best_partition(H)
    
    plt1=histogram(H, log=False, norm=True,cumu=0, n=10)
    plt1.xlabel('Relative frequencies')
    plt1.ylabel('Degree of the node')
    plt1.title('Histogram in the usual scale')
    plt1.savefig(save_path+'Hist_nolog'+'.jpg')
    plt1.show()
    
    plt2=histogram(H, log=True, norm=True,cumu=0, n=10)
    plt2.xlabel('Log frequencies')
    plt2.ylabel('Log scale degree')
    plt2.title('Histogram in Log scale')
    plt2.savefig(save_path+'Hist_Log'+'.jpg')
    plt2.show()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
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