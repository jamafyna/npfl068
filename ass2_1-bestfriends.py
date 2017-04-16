
import sys
import collections as col
import icu
import math
import random
import datetime

sin=sys.stdin
sout=sys.stdout 


DIST=50 # the distance between 2 words
LOW=10 # the number for disregarding: if word appears less than LOW times  



def getPMI(a,b,P_ij,P_i):
        if (a,b) not in P_ij: 
            print("debug 0")
            return 0
        else: return math.log(P_ij[a,b]/(P_i[a]*P_i[b]),2)
        

f=open(sys.argv[1],encoding="iso-8859-2",mode='rt')
wordsdata=f.read().splitlines() # given words
wordsuniq=col.Counter(wordsdata)
wn10=col.Counter({w:wordsuniq[w] for w in wordsuniq if wordsuniq[w]<LOW})
uniqbigrams=col.Counter(zip(wordsdata[:-1],wordsdata[1:])) # bigrams only from given words, not added start and end boundaries
wordcount=len(wordsdata)
bigramcount=wordcount-1
Pi={w : wordsuniq[w]/wordcount for w in wordsuniq} # Pi ... probability P(i)
Pij={u : uniqbigrams[u]/bigramcount for u in uniqbigrams} # Pij ... joint probability  P(i,j), j is immediately after the word i

#I=col.Counter({(u,v):math.log(Pij[u,v]/(Pi[u]*Pi[v]),2) for (u,v) in uniqbigrams if u not in wn10 and v not in wn10})
I=col.Counter({(u,v):math.log(Pij[u,v]/(Pi[u]*Pi[v]),2) for (u,v) in uniqbigrams if wordsuniq[u]>=LOW  and wordsuniq[v]>=LOW})
#I2=col.Counter({(u,v):getPMI(u,v,Pij,Pi) for (u,v) in uniqbigrams if u not in wn10 and v not in wn10})

print(I.most_common(20))
print(I.most_common(-20)) #nevyžaduje, ale je fajn

#------------po sem to funguje, odtud neni overene


Idis=col.Counter()
distant=col.Counter()
for i in range (0,wordcount-1):
    for j in range (1,DIST+1):
        if(i-j>=0):
            u=wordsdata[i-j]
            w=wordsdata[i]
            distant[u,w]+=1
            #if(w in w10 and u in w10):
            #    Idis[u,w]=getPMI(w,u)
totalcount=sum(distant.values())
Pdij={pair : distant[pair]/totalcount for pair in distant} # probability of distant words
Idis=col.Counter({(u,v):getPMI(u,v,Pdij,Pi) for (u,v) in distant if u not in wn10 and v not in  wn10})

#----2.varianta, pro to, kdy beru oba směry explicitně

# z hlediska psti a dal je jedno, zda pouzivame toto nebo vyse, protože v tomto bude každé slovo 2x, ale i 2x věší počet slov, tedy stejné výsledky
I2dis=col.Counter()
distant2=col.Counter()
for i in range (0,wordcount-1):
    for j in range (1,DIST+1):
        if(i-j>=0):
            u=wordsdata[i-j]
            w=wordsdata[i]
            distant2[u,w]+=1
        if(i+j<wordcount-1):
            u=wordsdata[i+j]
            w=wordsdata[i]
            distant2[w,u]+=1
            #if(w in w10 and u in w10):
            #    Idis[u,w]=getPMI(w,u)
totalcount2=sum(distant2.values())
Pdij2={pair : distant2[pair]/totalcount2 for pair in distant2} # probability of distant words
Idis2=col.Counter({(u,v):getPMI(u,v,Pdij2,Pi) for (u,v) in distant2 if u not in wn10 and v not in  wn10})

