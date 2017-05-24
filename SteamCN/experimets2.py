'''
Created on 24 may. 2017

@author: jorge
'''
import networkx as nx
# import community
from functions.Utils import clean_graph, load
import numpy as np
import matplotlib.pyplot as plt

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

H=load('Networks/final_cleared.net')
H = nx.Graph(H)
print(nx.info(H))

print('\n\ndatabase: ')
        
numbNodes=H.number_of_nodes()
numbEdges=H.number_of_edges()
        
print('Number of nodes: ' + str(numbNodes))
print('Number of edges: ' + str(numbEdges))

degrees = nx.degree(H).values()
        
print('Degree in formation: ' + 'Mean: ' + str(np.mean(degrees)) + ', Maximum: '+ str(max(degrees))  +' and Minimum: '+ str(min(degrees)))
        
clustering=nx.clustering(nx.Graph(H)).values()
print('Average clustering coefficient: ' + str(np.mean(clustering)))
        
assortativity=nx.degree_assortativity_coefficient(H)        
print('Assortativity: '+str(assortativity))
        
average_path, diameter = nx.average_shortest_path_length(H)
diameter=nx.diameter(H)
print('Average path length: '+str(average_path)+ '\nDiameter: '+str(diameter))
        
data_results=( numbNodes, numbEdges, np.mean(degrees), max(degrees), min(degrees), np.mean(clustering), assortativity, average_path, diameter)

#partition = community.best_partition(H)

plt1=histogram(H, log=False, norm=True,cumu=0, n=10)
plt1.show()
plt2=histogram(H, log=True, norm=True,cumu=0, n=10)
plt2.show()

print('Ploting the graph...')

np.random.seed(51111)
    
pos=nx.spring_layout(H)

plt.axis('off')
nx.draw_networkx(H,pos,with_labels=False)


'''
part = community.best_partition(G)
values = [part.get(node) for node in G.nodes()]
    
nx.draw_spring(G, 
                   cmap = plt.get_cmap('jet'),
                   node_color = values, 
                   #node_size=30, 
                   with_labels=False)
'''