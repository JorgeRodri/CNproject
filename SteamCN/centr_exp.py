
from functions.Utils import load, save, inverse_data
from functions.API import get_user_info, get_game_name
from operator import itemgetter
from collections import Counter, OrderedDict
import numpy as np
import matplotlib.pyplot as plt


def get_table(degree, eigen, close, btw, data):
    results=[]
    for i in [1,5,10,50,100]:
        N=i*len(data)/100
        c=degree.keys()[0:N]
        d1=obtain_info(c, data,1)
        
        c=eigen.keys()[0:N]
        d2=obtain_info(c, data,1)  
              
        c=close.keys()[0:N]
        d3=obtain_info(c, data, 1)
        
        c=btw.keys()[0:N]
        d4=obtain_info(c, data, 1)
        
        results.append([i,d1,d2,d3,d4])
    return results
    
def obtain_info(c, data,extra=0):
    t={}
    for i in c:
        t[i]=[data[i][0],len(data[i][1]),len(data[i][2])]
    if extra!=1:
        return t
    else:
        return [round(np.mean([l[0] for l in t.values()]),2), round(np.mean([l[1] for l in t.values()]),2), round(np.mean([l[2] for l in t.values()]),2)]
        

data=load('Data/dict_data.txt')
games_data=load('Data/inverse_data.txt')
centr_btw=load('centrality/betweenness_centrality.txt')
centr_btw_par=load('centrality/betweenness_centrality_parallel_pooling2.txt')
centr_degree=load('centrality/degree_centrality.txt')
centr_clos=load('centrality/closeness_centrality.txt')
centr_eigen=load('centrality/eigenvector_centrality.txt')

centr_btw=OrderedDict(sorted(centr_btw.items(), key=itemgetter(1), reverse=True))
centr_btw_par=OrderedDict(sorted(centr_btw_par.items(), key=itemgetter(1), reverse=True))
centr_degree=OrderedDict(sorted(centr_degree.items(), key=itemgetter(1), reverse=True))
centr_clos=OrderedDict(sorted(centr_clos.items(), key=itemgetter(1), reverse=True))
centr_eigen=OrderedDict(sorted(centr_eigen.items(), key=itemgetter(1), reverse=True))



"""plt.plot(centr_btw.values()[0:5000])
plt.show()

plt.plot(centr_btw_par.values())
plt.show()

plt.plot(centr_degree.values())
plt.show()

plt.plot(centr_clos.values())
plt.show()

plt.plot(centr_eigen.values())
plt.show()"""


#print centr_btw.keys()[0:10] #equal to the next so nice, there are only 7 that are repeated
c=set(centr_btw_par.keys()[0:10]+centr_degree.keys()[0:10]+centr_clos.keys()[0:10]+centr_eigen.keys()[0:10])

'''latex table
for i in range(10):
    print str(centr_degree.keys()[i])+' & '+str(centr_eigen.keys()[i])+' & '+str(centr_clos.keys()[i])+' & '+str(centr_btw_par.keys()[i])+' \\'
'''


"""games=[data[i][0] for i in data.keys()]
print 'mean of owned games: '+str(np.mean(games))

games=[len(data[i][1]) for i in data.keys()]
print 'mean of played bought games: '+str(np.mean(games))

games=[len(data[i][2]) for i in data.keys()]
print 'mean of played f2p games: '+str(np.mean(games))

n=5

c=centr_degree.keys()[0:n]
dict1=obtain_info(c, data)
print dict1.values()

c=centr_eigen.keys()[0:n]
dict1=obtain_info(c, data)
print dict1.values()

c=centr_clos.keys()[0:n]
dict1=obtain_info(c, data)
print dict1.values()

c=centr_btw_par.keys()[0:n]
dict1=obtain_info(c, data)
print dict1.values()
"""

wolo=get_table(centr_degree, centr_eigen, centr_clos, centr_btw_par, data)
print len(wolo)
print len(wolo[0])
#printing the table
with open('table.txt','w') as f:
    for i in wolo:
        line=''
        for j in i:
            line+=str(j)+ ' & '
        f.write(line+'\n')
        


