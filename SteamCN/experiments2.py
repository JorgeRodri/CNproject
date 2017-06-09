
import networkx as nx
# import community
from functions.Utils import clean_graph, load, save
from functions.API import get_game_name, get_user_info
import numpy as np
import matplotlib.pyplot as plt
import community
import random


def community_game_recomender(data, part):
    
    # Get random user's name
    key = [k for k in part]
    key_data = [k for k in data]
    index = random.sample(range(0, len(part)), 5)
    users = [key[i] for i in index]
    user_community = [part[u] for u in users]
    
    
    recomendationFree = {}
    recomendationPay = {}
    for usr in users:
        c = user_community[users.index(usr)]
        free_games = {}
        payment_games = {}
        community = [user for user in part if part[user] == c]      # user name of all user in the community
        for user in community:
            if user in key_data:
                for fgame in data[user][1]:
                    if fgame not in free_games:
                        free_games[fgame] = 1
                    else:
                        free_games[fgame] = free_games[fgame] + 1
                        
                for pgame in data[user][2]:
                    if pgame not in payment_games:
                        payment_games[pgame] = 1
                    else:
                        payment_games[pgame] = payment_games[pgame] + 1
            
        sorted_fgame = sorted(free_games, key=free_games.get, reverse=True)
        sorted_pgame = sorted(payment_games, key=payment_games.get, reverse=True)
        
        try:
            cleared_fgames =[game for game in sorted_fgame if game not in data[usr][1]]
            cleared_pgames =[game for game in sorted_pgame if game not in data[usr][2]]
            
            recomendationFree[usr] = cleared_fgames[:5]
            recomendationPay[usr] = cleared_pgames[:5]
                
        except KeyError:
            recomendationFree[usr] = sorted_fgame[:5]
            recomendationPay[usr] = sorted_pgame[:5]

    
    steam_id = '76561198067384609L'
    key = '2A526C7C2F3CEB0307B864A8DD15D320'     
    for rf in recomendationFree:
        recomendationFree[rf] = get_game_name(steam_id, key)[recomendationFree[rf]]
    for rf in recomendationPay:
        recomendationPay[rf] = get_game_name(steam_id, key)[recomendationPay[rf]]
   
          
    return recomendationFree, recomendationPay

def distance_recomender(G, data, part):
    key = [k for k in part]
    key_data = [k for k in data]
    find = False
    while (not find):
        index = random.sample(range(0, len(part)), 5)
        users = [key[i] for i in index]
        if set(users) <= set(key_data):
            find = True          
    users = [key[i] for i in index]
    user_community = [part[u] for u in users]
    
    recomendationFriend = {}
    recomendationFree   = {}
    recomendationPay    = {}
    
    for usr in users:
        c = user_community[users.index(usr)]
        
        neighbour = {}
        community = [user for user in part if part[user] == c]      # user name of all user in the community
        for user in community:
            if user in key_data:
                free_common = sum(1 for fgame in data[user][1] if fgame in data[usr][1])
                pay_common  = sum(1 for fgame in data[user][2] if fgame in data[usr][2])
                try:
                    neighbour[user] = (free_common+pay_common)/(len(data[usr][1])+len(data[usr][2]))
                except ZeroDivisionError:
                    neighbour[user] = (free_common+pay_common)/(len(data[user][1])+len(data[user][2])+1)
                    
        sorted_nb = sorted(neighbour, key=neighbour.get, reverse=False)
        
        free_games = {}
        payment_games = {}
        for nb in sorted_nb[:10]:
            for fgame in data[nb][1]:
                if fgame not in free_games:
                    free_games[fgame] = 1
                else:
                    free_games[fgame] = free_games[fgame] + 1
            for pgame in data[nb][2]:
                if pgame not in payment_games:
                    payment_games[pgame] = 1
                else:
                    payment_games[pgame] = payment_games[pgame] + 1
        
        sorted_fgame = sorted(free_games, key=free_games.get, reverse=True)
        sorted_pgame = sorted(payment_games, key=payment_games.get, reverse=True)
        try:
            cleared_fgames = [game for game in sorted_fgame if game not in data[usr][1]]
            cleared_pgames = [game for game in sorted_pgame if game not in data[usr][2]]
            cleared_nb     = [nb for nb in sorted_nb if nb not in G.edge[usr]]
            recomendationFree[usr] = cleared_fgames[:5]
            recomendationPay[usr] = cleared_pgames[:5]
            recomendationFriend[usr] = cleared_nb[:5]
        except KeyError:
            recomendationFree[usr] = sorted_fgame[:5]
            recomendationPay[usr] = sorted_pgame[:5]
            recomendationFriend[usr] = sorted_nb[:5]
    
    steam_id = '76561198067384609L'
    key = '2A526C7C2F3CEB0307B864A8DD15D320'     
    for rf in recomendationFree:
        recomendationFree[rf] = get_game_name(steam_id, key)[recomendationFree[rf]]
    for rf in recomendationPay:
        recomendationPay[rf] = get_game_name(steam_id, key)[recomendationPay[rf]]
    for rf in recomendationFriend:
        recomendationFriend[rf] = get_game_name(steam_id, key)[recomendationFriend[rf]]
         
    return recomendationFriend,recomendationFree, recomendationPay



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
steam_id = '76561198067384609L'
key = '2A526C7C2F3CEB0307B864A8DD15D320'
print 'Recomendation by communities\n'
for r in recomendationFree:
    print 'user:',get_user_info(steam_id, key)[r]
    #print '\tuser:',r
    print '\t\t Free games:',recomendationFree[r]
    print '\t\t Payment games:',recomendationPay[r]

recomendationFriend,recomendationFree, recomendationPay = distance_recomender(G,data, part)  
print 'Recomendation by distance\n'
for r in recomendationFree:
    print 'user:',get_user_info(steam_id, key)[r]
    #print '\t User:',r
    print '\t\t Suggested Friends:',recomendationFriend[r]
    print '\t\t Free games:',recomendationFree[r]
    print '\t\t Payment games:',recomendationPay[r]    
    

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