
import sys
import collections as col
import icu
import math
import random
import datetime

sin=sys.stdin
sout=sys.stdout 






def getPMI(a,b):
        if (a,b) not in Pij: 
            print("debug 0")
            return 0
        else: return math.log(Pij[a,b]/(Pi[a]*Pi[b]))
        

f=open(sys.argv[1],encoding="iso-8859-2",mode='rt')
wordsdata=f.read().splitlines() # given words
wordsuniq=col.Counter(wordsdata)
w10=col.Counter({w:wordsuniq[w] for w in wordsuniq if wordsuniq[w]>9})
uniqbigrams=col.Counter(zip(wordsdata[:-1],wordsdata[1:])) # bigrams only from given words, not added start and end boundaries
wordcount=len(wordsdata)
bigramcount=wordcount-1
Pi={w : wordsuniq[w]/wordcount for w in wordsuniq} # Pi ... probability P(i)
Pij={u : uniqbigrams[u]/bigramcount for u in uniqbigrams} # Pij ... joint probability  P(i,j), j is immediately after the word i

I=col.Counter({(u,v):math.log(Pij[u,v]/(Pi[u]*Pi[v])) for (u,v) in uniqbigrams if u in w10 and v in w10})

print(I.most_common(20))
print(I.most_common(-20)) #nevyžaduje, ale je fajn

#------------po sem to funguje

#distance max 50 - MUSÍ SE POČÍTAT JINÝM ZPŮSOBEM, NAPŘ NEVYUŽÍVAT P(A,B) JAKO PST PO SOBĚ JDOUCÍCH SLOV, ALE NAPŘ PST, ŽE JE MEZI SLOVY DISTANCE MAX 50 - ZEPTAT SE
Idis=col.Counter()
for i in range (0,wordcount-1):
    for j in range (1,50):
        if(i+j<wordcount):
            w=wordsdata[i]
            u=wordsdata[i+j]
            if(w in w10 and u in w10):
                Idis[u,w]=getPMI(w,u)

