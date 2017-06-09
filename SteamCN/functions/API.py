#!/experiments2/local/bin/python2.7
# encoding: utf-8
'''
functions.API -- shortdesc

functions.API is a description

It defines functions for obtaining data from the API

@author:     Ricard Borrull and Jorge Rodriguez
@copyright:  2017 Jorge and Ricard. All rights reserved.

@contact:    user_email
@deffield    updated: Updated
'''
import urllib2
import json

def get_friends(steam_id, key):
    request = 'https://api.steampowered.com/ISteamUser/GetFriendList/v1?steamid={steamid}&key={key}'
    r = urllib2.urlopen(request.format(key=key,steamid=steam_id))
    string = r.read().decode('utf-8')
    list_of_friends = [x['steamid'] for x in json.loads(string)['friendslist']['friends']]
    return list_of_friends

def get_games(steam_id, key, f2p=False):
    request = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={key}&steamid={steamid}&format=json'
    r = urllib2.urlopen(request.format(key=key,steamid=steam_id))
    string = r.read().decode('utf-8')
    list_of_games = json.loads(string)['response']['games']
    number_of_games = json.loads(string)['response']['game_count']
    list_of_played_games=[x['appid'] for x in list_of_games if x['playtime_forever']>60]
    if f2p:
        request = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={key}&steamid={steamid}&include_played_free_games=1&format=json'
        r = urllib2.urlopen(request.format(key=key,steamid=steam_id))
        string = r.read().decode('utf-8')
        list_of_games = json.loads(string)['response']['games']
        number_of_games = json.loads(string)['response']['game_count']
        list_of_f2p=[x['appid'] for x in list_of_games if x['playtime_forever']>60 and x['appid'] not in list_of_played_games]
    else:
        list_of_f2p = []
    return number_of_games, list_of_played_games, list_of_f2p

def get_game_name(app_id, key):
    request = 'http://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?key={key}&appid={appid}'
    r = urllib2.urlopen(request.format(key=key,appid=app_id))
    string = r.read().decode('utf-8')
    try:
        name = json.loads(string)["game"]["gameName"]
    except KeyError:
        name=app_id
        print('The server returned invalid data, name='+str(app_id))
    return name

def get_user_info(steam_id, key):
    request = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={key}&steamids={steamid}'
    r = urllib2.urlopen(request.format(key=key,steamid=steam_id))
    string = r.read().decode('utf-8')
    info = json.loads(string)['response']['players'][0]
    return info