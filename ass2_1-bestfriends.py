
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
        """ 
        Returns Pointwise Mutual Information
        """
        if (a,b) in P_ij: # it should be everytime true
            return math.log(P_ij[a,b]/(P_i[a]*P_i[b]),2)
        
if len(sys.argv)!=2:
    sys.exit('Not correct arguments, please run with 1 argument:  input-file in .txt')
    
f=open(sys.argv[1],encoding="iso-8859-2",mode='rt')
wordsdata=f.read().splitlines() # given words
wordsuniq=col.Counter(wordsdata)
wn10=col.Counter({w:wordsuniq[w] for w in wordsuniq if wordsuniq[w]<LOW}) # words which appears less then LOW times in the corpus data
uniqbigrams=col.Counter(zip(wordsdata[:-1],wordsdata[1:])) # bigrams only from given words, no start and end boundaries
wordcount=len(wordsdata)
bigramcount=wordcount-1
Pi={w : wordsuniq[w]/wordcount for w in wordsuniq} # Pi ... probability P(i)
Pij={u : uniqbigrams[u]/bigramcount for u in uniqbigrams} # Pij ... joint probability  P(i,j), j is immediately after the word i

#I=col.Counter({(u,v):math.log(Pij[u,v]/(Pi[u]*Pi[v]),2) for (u,v) in uniqbigrams if wordsuniq[u]>=LOW  and wordsuniq[v]>=LOW})
I=col.Counter({(u,v):getPMI(u,v,Pij,Pi) for (u,v) in uniqbigrams if u not in wn10 and v not in wn10})

print(I.most_common(20))
print(I.most_common(-20)) #nevyžaduje, ale je fajn

#------------po sem to funguje, odtud si nejsem jistá


distant=col.Counter() # distant[u,w]=c...this pair appears c times in text with distance 1-50
for i in range (0,wordcount): # if there is no start and end token, it is the same to compute only one direction or both directions
    for j in range (1,DIST+1):
        if(i-j>=0):
            u=wordsdata[i-j]
            w=wordsdata[i]
            distant[u,w]+=1
totalcount=sum(distant.values())
Pdij={pair : distant[pair]/totalcount for pair in distant} # probability of distant words
Idis=col.Counter({(u,v):getPMI(u,v,Pdij,Pi) for (u,v) in distant if u not in wn10 and v not in  wn10})
#pozor na to, jestli mám správně Pi - jestli i ta se nemusí upravit, protože se  krajní slova používají jinak
#----2.varianta, pro to, kdy beru oba směry explicitně

# z hlediska psti a dal je jedno, zda pouzivame toto nebo vyse, protože v tomto bude každé slovo 2x, ale i 2x věší počet slov, tedy stejné výsledky
I2dis=col.Counter()
distant2=col.Counter()
for i in range (0,wordcount):#měla jsem wordcount-1, ale to nedává smysl!
    for j in range (1,DIST+1):
        if(i-j>=0):
            u=wordsdata[i-j]
            w=wordsdata[i]
            distant2[u,w]+=1
        if(i+j<wordcount-1):
            u=wordsdata[i+j]
            w=wordsdata[i]
            distant2[w,u]+=1
totalcount2=sum(distant2.values())
Pdij2={pair : distant2[pair]/totalcount2 for pair in distant2} # probability of distant words
Idis2=col.Counter({(u,v):getPMI(u,v,Pdij2,Pi) for (u,v) in distant2 if u not in wn10 and v not in  wn10})
print(Idis.most_common(20))
print(Idis2.most_common(20)) 
