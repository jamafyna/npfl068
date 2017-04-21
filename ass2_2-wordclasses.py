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

# otázka: kde se mi projeví pravděpodobnostní rozdělení (tj. když mám brát v potaz i slova mající nižší výskyt než 10, ale když psi, se kterými pracuji, jsou jen pro classes?)

def getPMI(a,b,P_ij,P_i):
        if (a,b) not in P_ij: 
            print("debug 0")
            return 0
        else: return math.log(P_ij[a,b]/(P_i[a]*P_i[b]),2)

def maximizeL():
#we need to maximize I(D,E) for 
        return 0

def merge(k,l):
        """
        merge two classes k and l into one class
        """    
        return 0

def findmerge():
        """
        find two classes for which MI (I(D,E)) is maximal
        """
        return 0,0           

def getMI(bigC):
        """
        returns I(D,E)
        input: bigC - bigrams of classes, ideally Counter
        """
        return sum([p(d,e) * math.log(p(d,e)/(p(d)*p(e)),2) for (d,e) in bigC])
       # p bude nejspíš c_ij a cl_i,cr_i 


f=open(sys.argv[1],encoding="iso-8859-2",mode='rt')
data=[l.split('/',1) for l in f.read().splitlines()]  # items in format: word,speech-tag which can contains '/'
#for (word,tag) in data...

data_words=[word for (word,tag) in data]

wordsall=data_words[:8000]
bigramsall=[b for b in zip(wordsall[:-1],wordsall[1:])]
uniqbigrams=col.Counter(bigramsall) # bigrams only from given words, not added start and end boundaries

uniqwords=col.Counter(wordsall)

words=[w for w in data_words[:8000] if uniqwords[w]>=10]
classes=[c for c in words] # initialization, starts with each word in its own class
uniqclasses=col.Counter(classes)
w10=[w for w in wordsall if uniqwords[w]>=10]
big10=[(u,v) for (u,v) in uniqbigrams if uniqwords[u]>=10 and uniqwords[v]>=10]

#
#pp2ch=
print(sum([uniqbigrams[p,q]/len(uniqbigrams)*math.log(uniqbigrams[p,q]/len(uniqbigrams)/(uniqwords[p]/len(uniqwords)*uniqwords[q]/len(uniqwords)),2) for (p,q) in uniqbigrams]))

print(sum([uniqbigrams[p,q]/len(big10)*math.log(uniqbigrams[p,q]/len(big10)/(uniqwords[p]/len(w10)*uniqwords[q]/len(w10)),2) for (p,q) in col.Counter(big10)]))
big10col=col.Counter(big10)
word10col=col.Counter(w10)
pclass_i={u:word10col[u]/len(word10col) for u in word10col}
pbigclass_ij={(u,v):big10col[u,v]/word10col[v]*pclass_i[u] for (u,v) in big10col}
print(sum([pbigclass_ij[u,v]*math.log(pbigclass_ij[u,v]/(pclass_i[u]*pclass_i[v]),2) for (u,v) in pbigclass_ij]))

s=0
N=len(wordsall)
for x in uniqwords:
    for c in word10col:
        s+=uniqwords[x]/(N-1)*math.log(N*len(word10col)/((N-1)*word10col[c]),2)
        
print(s)
s=0
print(sum([math.log(uniqbigrams[u,v]/(uniqwords[u]*uniqwords[v]),2)for (u,v) in bigramsall]))
N=len(wordsall)
print(sum([uniqbigrams[d,e]/(N-1)*math.log(uniqbigrams[d,e]*N*N/((N-1)*uniqwords[d]*uniqwords[e]),2)  for (d,e) in uniqbigrams]))

# ------------------u------initialization -----------------------------
N=len(data_words)-1 # count of bigrams in data
#Hist=[] # history of merges: Hist(k)=(a,b) merged when the remaining number of classes was k
#c_ij= #bigram class counts (updated)
#cl_i= # unigram left counts (updated)
#cr_i= # unigram right counts (updated)
#L_ab= # table of looses, upper-right triangle (updated)
#s_a= # subtraction subterms (optionaly updated)
#q_ij = #subterms involving a log (opt. updated)

# trochu jine, nez nize, spravna definice je na str. 124
#c_ij=col.Counter(zip(classes[:-1],classes[1:]))
#cl_i=col.Counter(classes[:-1])
#cr_i=col.Counter(classes[1:])


#wordsuniq=col.Counter(wordsdata)
#wn10=col.Counter({w:wordsuniq[w] for w in wordsuniq if wordsuniq[w]<LOW})
#uniqbigrams=col.Counter(zip(wordsdata[:-1],wordsdata[1:])) # bigrams only from given words, not added start and end boundaries
#wordcount=len(wordsdata)
#bigramcount=wordcount-1

