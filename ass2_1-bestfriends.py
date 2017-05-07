
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

I=col.Counter({(u,v):getPMI(u,v,Pij,Pi) for (u,v) in uniqbigrams if u not in wn10 and v not in wn10})

print("\nPOINTWISE MUTUAL INFORMATION FOR ALL THE POSSIBLE PAIRS (which appear 10 and more times), first 20 of them:")
#for ((u,v),i) in I.most_common(20): print(i,'\t',u," ",v)
for ((u,v),i) in I.most_common(20): print(i,'&',u,"&",v, '\\\\') # latex format to table

f=open("results-pairs-all-"+sys.argv[1], 'wt')
for ((u,v),i) in I.most_common():
    f.write(str(i)+'\t'+str(u)+' '+str(v)+'\n')
f.close()
# -------------- for distant words ------------------------------

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

print("\nPOINTWISE MUTUAL INFORMATION FOR DISTANT WORDS, first 20")
for ((u,v),i) in Idis.most_common(20): print(i,'&',u,"&",v, '\\\\') #latex table format
#for ((u,v),i) in Idis.most_common(20): print(i,'\t',u," ",v)

f=open("results-distance-all-"+sys.argv[1], 'wt')
for ((u,v),i) in Idis.most_common():
    f.write(str(i)+'\t'+str(u)+' '+str(v)+'\n')
f.close()
