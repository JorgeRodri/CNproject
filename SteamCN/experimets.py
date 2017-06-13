

from functions.Utils import load, save, inverse_data
from functions.API import get_user_info, get_game_name
from operator import itemgetter
from collections import Counter, OrderedDict
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import networkx as nx
import time
from math import sqrt

def takeSecond(elem):
    return elem[1]

def inv_dict(my_map):
    inv_map = {}
    for k, v in my_map.iteritems():
        inv_map[v] = inv_map.get(v, [])
        inv_map[v].append(k)
    return inv_map  

def index(u1, u2):
    union=set(u1+u2)
    intersection=[ game for game in u1 if game in u2]
    if len(union)==0:
        return 0
    else:
        return float(len(intersection))/len(union)
    
def find_measure(data, nodes):
    users=nodes
    values=0
    n=0
    while len(users)>1:
        u1=users.pop()
        g1=data[u1]
        for u2 in users:
            g2=data[u2]
            values+=index(g1,g2)
            n+=1
    return float(values)/n


def data_needed(com_dict,n):
    forbidden_games=['730', '433850']
    data={}
    for comm in com_dict.keys():
        x=com_dict[comm]
        aux=x[1]
        aux.update(x[2])
        d = OrderedDict(sorted(data.items(), key=itemgetter(1)))
        helper=d.keys()
        for i in forbidden_games:
            try:
                helper.remove(i)
            except ValueError:
                pass
        data[comm]=helper[0:n]
    return data
        
def sim(C1,C2):
    s=set(C1.keys()+C2.keys())
    l=[]
    for game in s:
        try:
            a=C1[game]
        except KeyError:
            a=0
        try:
            b=C2[game]
        except KeyError:
            b=0
        d=(a-b)^2
        l.append(d)
    return sqrt(sum(l))/len(s)
    
    
with open('claveSteam.txt', 'rb') as f: # Get at http://steamcommunity.com/dev/registerkey
         key=f.read()

G=nx.Graph(load('Networks/final_cleared.net'))
com_dict=load('Data/Community_dict.txt')
com_dict_lists=load('Data/Community_dict_lists.txt')

communities=load('Data/Communities.txt')
data=load('Data/dict_data.txt')
#inverse_data()
games_data=load('Data/inverse_data.txt')

"""aux=[data[i][0] for i in data.keys()]
aux.sort()
print(aux[-15:-1])
aux=aux[0:len(aux)*95/100]

plt.hist(aux, 50,cumulative=0, normed=1)
plt.show()"""
print('Files loaded.')

print 'checking powerlaw'

degrees=G.degree().values()
D, pvalue =stats.kstest(degrees, stats.powerlaw.rvs)

if pvalue<0.05:
    print 'Follows a Powerlaw distribution.'
print 'done, next'


print 'Most Played Games:'

x=[(i,games_data[i][1], games_data[i][0]) for i in games_data.keys()]


sorted_x = sorted(x, reverse=True, key=takeSecond)

print sorted_x[0:13]
names=[get_game_name(str(g_id), key) for g_id, users, f2p in sorted_x[0:13] ]
print 'Most played games: '
print names
print '\n'

n=0

#com_dict has mean of games owned, games in the community, 


games_count=[com_dict_lists[i][0] for i in range(len(com_dict_lists))]
comm_games=[(np.mean(g), np.std(g)) for g in games_count]
print 'Info of games owned by community: ' +str(comm_games[45:51])
print 'Number of communities= '+str(max(communities.values())+1)


dict_forsim={}
for user in data.keys():
    dict_forsim[user]=data[user][1]+data[user][2]
    
"""t1=time.time()
measure_for_network=find_measure(dict_forsim,data.keys())
t2=time.time()
print 'Measure for the whole network: '+str(measure_for_network)+ 'in a time of: '+ str(t2-t1)"""

print 'Calculation for commm'
t1=time.time()
communities_values=[]
members_in_community=inv_dict(communities)
for community in members_in_community.keys():
    nodes=members_in_community[community]
    m=find_measure(dict_forsim, nodes)
    communities_values.append(m)
    #print'For community '+str(community)+ ' the value is: '+str(m)
t2=time.time()

save(communities_values, 'centrality/comm_val.txt')
print 'Measure for the communities network: '+str(communities_values)
print 'Mean of: '+str(np.mean(communities_values))
print 'In a time of: '+ str(t2-t1)

print stats.ttest_1samp(communities_values, 0.14601681)

"""c=Counter(communities.values())
print 'Mean of users in a community: ' + str(np.mean(c.values()))

l={}
for comm in com_dict.keys():
    x=com_dict[comm]
    l[comm]=[float(i)/c[comm] for i in x[1].values()] + [float(i)/c[comm] for i in x[2].values()]


measure2=0
users=l.keys()
n=0
while len(users)>1:
    u1=users.pop()
    g1=l[u1]
    for u2 in users:
        g2=l[u2]
        values+=sim(g1,g2)
        n+=1
print 'Found the measure: ' + str(measure2/n)"""


'''    
m=sim(C1,C2)
s=np.zeros((len(com_dict),len(com_dict)))
data = data_needed(com_dict,12)



for i in data.keys():
    for j in data.keys():
        s[i,j]=sim(data[i],data[j])
print s
'''    
'''
horrible prints
for comm in com_dict.keys():
    n+=1
    x=com_dict[comm]
    print('Mean of games for comm: '+str(x[0]))
    print('Most played games :')
    sorted_x=sorted(x[1].items(), reverse=True, key=operator.itemgetter(1))
    print sorted_x[0:12]
    names=[get_game_name(str(g_id), key) for g_id, users in sorted_x[0:12] ]
    print(names)
    print('Most played free games :')
    sorted_x=sorted(x[2].items(), reverse=True, key=operator.itemgetter(1))
    print sorted_x[0:12]
    names=[get_game_name(str(g_id), key) for g_id, users in sorted_x[0:12] ]
    print names
    print '\n'
#    if n*24%200==0:
#        time.sleep(60)
#        print 'Waiting in case the server blocks us.'
'''
