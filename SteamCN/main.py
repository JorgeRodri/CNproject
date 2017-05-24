'''
Created on 22 may. 2017

@author: Ricard and Jorge
'''
from functions.Utils import save, load
from functions.generators import download_games

if __name__=='__main__':
    with open('claveSteam.txt', 'rb') as f: # Get at http://steamcommunity.com/dev/registerkey
        key=f.read()
    #G=load('Networks/final_cleared.net')
    pending=load('Data/pending6.txt')
    data, pending, count=download_games(pending, key,w8_time=(0,120))
    save(data, 'Data/data7.txt')
    save(pending, 'Data/pending7.txt')
    print('\n\n\nDone for: '+str(count))