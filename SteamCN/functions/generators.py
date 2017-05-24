#!/usr/local/bin/python2.7
# encoding: utf-8
'''
Created on 22 may. 2017

functions.generators -- shortdesc

functions.generators functions that construct the graphs

@author:     Ricard Borrull and Jorge Rodriguez
@copyright:  2017 Jorge and Ricard. All rights reserved.

@contact:    user_email
@deffield    updated: Updated
'''
from API import get_friends
from API import get_games
import urllib2
import time

def construct_graph(G, nodes, key, request_limit=1000000, w8_time=(1,100), waiting=True):
    searched_nodes = [x for x in G.nodes() if x not in nodes]
    aux=0 #in case we have explore the hole graph
    count = 0
    while len(nodes)>0 and count<request_limit:
        cur_id = nodes.pop()
        if cur_id not in searched_nodes:
            G.add_node(cur_id)
            friends_list = []
                
            # Private profiles and reaching maximum requests can cause exceptions 
            try:
                friends_list = get_friends(cur_id, key)
            except urllib2.HTTPError:
                pass
            except urllib2.URLError:
                nodes.append(cur_id)
                print('Request limit reached, returning the obtained graph... Waiting is required. Done: '+str(len(searched_nodes))+' Pending: '+str(len(nodes)))
                break
                    
            for friend in friends_list:
                nodes.append(friend)
                G.add_edge(cur_id,friend)
            count+=1
            searched_nodes.append(cur_id)
            time.sleep(w8_time[0]) # To be polite to Valve's servers
            # this lines are to get track of the construction of the graph and also waiting since the limit of the server is 200 requests over 5 minutes
            if waiting and count%200==0: 
                if len(G.nodes())==aux:
                    count=1000000
                    break
                aux=len(G.nodes())
                print('\n Total size of the graph: '+str(aux))
                print('Nodes visted: '+str(len(searched_nodes)))
                print('Waiting 100 seconds... for the '+str(count/200)+'th time.')
                time.sleep(w8_time[1]) # To be polite to Valve's servers
    return G, nodes, count

def download_games(pending, key,count_limit=1000000, w8_time=(1,45), waiting=True):
    data=[]
    t1=time.time()
    count=0
    
    while len(pending)>0 and count<count_limit:
        i=pending.pop()
        #profiles with no games and reaching maximum request can cause an exception
        try:
            games, list_of_games, list_of_f2p = get_games(i,key,True)
        except KeyError:
            games=0
            list_of_games=[]
        except urllib2.URLError:
            pending.append(i)
            print('Request limit reached, returning the obtained data... Waiting is required. Done: '+str(len(data))+' Pending: '+str(len(pending)))
            break
        user=[i, games, list_of_games, list_of_f2p]
        count+=1
        data.append(user)
        time.sleep(w8_time[0]) # To be polite to Valve's servers
        #to get track of the information download and also waiting since the limit of the server is 200 requests over 5 minutes
        if waiting and count%100==0:
            t2=time.time()
            print('\nWaiting...')
            print 'Counter value= '+str(count)
            print 'Needed time for last 100: '+str(t2-t1)
            print 'Size of the data: '+str(len(data))
            time.sleep(w8_time[1]) # To be polite to Valve's servers
            t1=time.time()
    
    return data, pending, count
    

        

                    