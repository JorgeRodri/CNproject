

from functions.Utils import load, save, inverse_data
from functions.API import get_user_info, get_game_name
import operator
from collections import Counter
from numpy import mean

def takeSecond(elem):
    return elem[1]

    
    
with open('claveSteam.txt', 'rb') as f: # Get at http://steamcommunity.com/dev/registerkey
         key=f.read()

#G=nx.Graph(load('Networks/final_cleared.net'))
com_dict=load('Data/Community_dict.txt')
communities=load('Data/Communities.txt')
#data=load('Data/dict_data.txt')
inverse_data()
games_data=load('Data/inverse_data.txt')
    
print('Files loaded.')

x=[(i,games_data[i][1], games_data[i][0]) for i in games_data.keys()]


sorted_x = sorted(x, reverse=True, key=takeSecond)


names=[get_game_name(str(g_id), key) for g_id, users, f2p in sorted_x[0:12] ]
print 'Most played games: '
print names
print '\n'

n=0

c=Counter(communities.values())
l={}
for comm in com_dict.keys():
    n+=1
    x=com_dict[comm]
    l[comm]=[float(i)/c[comm] for i in x[1].values()] + [float(i)/c[comm] for i in x[2].values()]
    
for i in l.keys():
    l[i].sort(reverse=True)
    l[i] = mean(l[i][0:12])
print l
    
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
