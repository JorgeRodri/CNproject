
import networkx as nx
# import community
from functions.Utils import clean_graph, load, save
import numpy as np
import matplotlib.pyplot as plt
import community
import random
import operator
from sqlalchemy.sql.expression import false

def community_game_recomender(data, part):
    
    # Get random user's name
    key = [k for k in part]
    key_data = [k for k in data]
    index = random.sample(range(0, len(part)), 5)
    users = [key[i] for i in index]
    user_community = [part[u] for u in users]
    
    
    recomendationFree = {}
    recomendationPay = {}
    for c in user_community:
        free_games = {}
        payment_games = {}
        community = [user for user in part if part[user] == c]      # user name of all user in the community
        for user in community:
            if user+"\r" in key_data:
                for fgame in data[user+"\r"][1]:
                    if fgame not in free_games:
                        free_games[fgame] = 1
                    else:
                        free_games[fgame] = free_games[fgame] + 1
                        
                for pgame in data[user+"\r"][2]:
                    if pgame not in payment_games:
                        payment_games[pgame] = 1
                    else:
                        payment_games[pgame] = payment_games[pgame] + 1
            
        sorted_fgame = sorted(free_games, key=free_games.get, reverse=True)
        sorted_pgame = sorted(payment_games, key=payment_games.get, reverse=True)
        
        try:
            cleared_fgames =[game for game in sorted_fgame if game not in data[users[user_community.index(c)]+"\r"][1]]
            cleared_pgames =[game for game in sorted_pgame if game not in data[users[user_community.index(c)]+"\r"][2]]
            
            recomendationFree[users[user_community.index(c)]] = cleared_fgames[:5]
            recomendationPay[users[user_community.index(c)]] = cleared_pgames[:5]
                
        except KeyError:
            recomendationFree[users[user_community.index(c)]] = sorted_fgame[:5]
            recomendationPay[users[user_community.index(c)]] = sorted_pgame[:5]
            
    return recomendationFree, recomendationPay

def distance_recomender(data, part):
    
    key = [k for k in part]
    key_data = [k for k in data]
     
    index = random.sample(range(0, len(part)), 5)
    users = [key[i] for i in index]
    user_community = [part[u] for u in users]
     
    for c in user_community:
        community = [user for user in part if part[user] == c]      # user name of all user in the community
        for user in community:
            if user+"\r" in key_data:
                for fgame in data[user+"\r"][1]:
                    a = 'b' 

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


G=nx.read_pajek("Networks/final_cleared.net")

data=load('Data/dict_data.txt')
print(nx.info(G))

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

recomendationFree, recomendationPay = community_game_recomender(data, part)
print '\n'
for r in recomendationFree:
    print 'user:',r
    print '\t Free games:',recomendationFree[r]
    print '\t Payment games:',recomendationPay[r]

  
        
    

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



'''
nx.draw_spring(H,
                   cmap=plt.get_cmap('jet'),
                   node_color=values,
                   node_size=30,
                   with_labels=False)

plt.show()
'''