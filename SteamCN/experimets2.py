
import networkx as nx
# import community
from functions.Utils import clean_graph, load, save
import numpy as np
import matplotlib.pyplot as plt
import community

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


G=nx.read_pajek("Networks/demo.net")
print(nx.info(G))
H = clean_graph(G)

H = nx.Graph(G)
# nx.write_pajek(H, "Networks/demo2clean.net")
print(nx.info(H))


print('\n\ndatabase: ')       
numbNodes=H.number_of_nodes()
numbEdges=H.number_of_edges()
        
print('Number of nodes: ' + str(numbNodes))
print('Number of edges: ' + str(numbEdges))

degrees = nx.degree(H).values()
 
part = community.best_partition(H)
values = [part.get(node) for node in H.nodes()]
'''
f = open('Networks/demo_communities1.clu', 'w')
f.write("*Vertices "+ str(len(values))+"\n")
for i in values:
    f.write(str(i+1)+"\n")
f.close()

values.sort()
f = open('Networks/demo_communities2.clu', 'w')
f.write("*Vertices "+ str(len(values))+"\n")
for i in values:
    f.write(str(i+1)+"\n")
f.close()
'''
nx.draw_spring(H,
                   cmap=plt.get_cmap('jet'),
                   node_color=values,
                   node_size=30,
                   with_labels=False)

plt.show()