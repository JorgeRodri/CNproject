

from functions.Utils import load, save, inverse_data
from functions.API import get_user_info, get_game_name


with open('claveSteam.txt', 'rb') as f: # Get at http://steamcommunity.com/dev/registerkey
         key=f.read()

#G=nx.Graph(load('Networks/final_cleared.net'))
Com_dict=load('Data/Community_dict.txt')
#data=load('Data/dict_data.txt')
inverse_data()
games_data=load('Data/inverse_data.txt')
    
print('Files loaded.')

def takeSecond(elem):
    return elem[1]

x=[(i,games_data[i][1], games_data[i][0]) for i in games_data.keys()]


sorted_x = sorted(x, reverse=True, key=takeSecond)
print sorted_x[0:10]



names=[get_game_name(str(g_id), key) for g_id, users, f2p in sorted_x[0:10] ]
print names