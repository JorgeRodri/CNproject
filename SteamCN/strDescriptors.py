'''
Created on 24 may. 2017

@author: jorge
'''
import networkx as nx
import community
from functions.Utils import load, save
import numpy as np
import matplotlib.pyplot as plt
import time
from setuptools.sandbox import save_path

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

if __name__=='__main__':
    save_path='Structural_descriptors/'
    H=load('Networks/final_cleared.net')
    H=nx.Graph(H)
    
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

    
    
