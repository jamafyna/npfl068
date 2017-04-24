import sys
import collections as col
import icu
import math
import random
import datetime

sin=sys.stdin
sout=sys.stdout 



# otázka: kde se mi projeví pravděpodobnostní rozdělení (tj. když mám brát v potaz i slova mající nižší výskyt než 10, ale když psi, se kterými pracuji, jsou jen pro classes?)


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



# co chci:
# spočítat MI = sum([ c(d,e)/(N-1) * math.log((c(d,e)/(N-1))/(c(d)*c(e)/(N*N)),2)  for (d,e) in classes]) - zjistit, jestli je vždy N nebo jestli jde o aktuální počet tříd a aktuální počet bigramů tříd
# algoritmus:
# 1. inicializace: každé slovo ve  vlastní třídě
# 2. dokud není jen 1 třída (s výskytem >=10) tak opakuj:
# 3. najdi 2 třídy k,l, které sloučíš: zkus je sloučit + spočti maximální MI (= spočti minimální změnu MI)
# 4. sluč k,l
# 
# hodila by se datová struktura, ve které budu mít zahešované/uložené dvojice tříd, které se vyskytují po sobě a která vrací v konstatním čísle odpověď na dotaz q(c1,c2)  a zároveň vrací konstantně všechny prvky q(c1,*) a q(*,c2) - vždy po sloučení tříd by šlo zaktualizovat jen příslušné "řádky" a "sloupce"

# hloupá implementace:

# chytrá implementace:
def getmergedI(d,e,s):
        return
def getlossI(d,e):
        """
        Returns loss MI if d and e would be merged
        """
        new_count=classcount-1
        new_bi_count=0
#sum of loss MI of right neighbors of d, e
        s1=sum([(bi_class(d,s)+bi_class(e,s))*math.log((bi_class(d,s)+bi_class(e,s))*new_count**2)/(new_bi_count*(classes(d)+classes(e))*classes(s),2) for s in rightneib(a)+rightneib(b) if (s!=d and s!=e)])
#sum of loss MI of left neighbors of d, e
        s2=sum([(bi_class(s,d)+bi_class(s,e))*math.log((bi_class(s,d)+bi_class(s,e))*new_count**2)/(new_bi_count*(classes(d)+classes(e))*classes(s),2) for s in leftneib(a)+leftneib(b) if (s!=d and s!=e)])
# due to s=d or s=e
        caa=bi_class(e,e)+bi_class(e,d)+bi_class(d,e)+bi_class(d,d)
        ca=classes(e)+classes(d)
        s3=caa*math.log(caa*(new_count**2)/((ca**2)*new_bi_count),2)
        return (s1+s2+s3)/new_bi_count
        

def gettwoclasses():
        c1=[]
        c2=[]
        minI=float("inf")
        for d in classes:
            for e in classes: 
                temp=getlossI(d,e) 
                if minI>temp: 
                    minI=temp
                    c1=d
                    c2=e
        return (c1,c2)

def mergetwoclasses(d,e):
        #merge e into d
        for l in leftneib(e):
            bi_class[l,d]+=bi_class[l,e]
        for r in rightneib(e):
            bi_class[d,r]+=bi_class[e,r]
#možná opět PIE
        classes[d]+=classes[e]
        rightneib[d]+=set(rightneib[d]+rightneib[e])
        leftneib[d]+=set(leftneib[d]+leftneib[e])
        # remove
        for r in 

        return





f=open(sys.argv[1],encoding="iso-8859-2",mode='rt')
data=[l.split('/',1) for l in f.read().splitlines()]  # items in format: word,speech-tag which can contains '/'
#for (word,tag) in data...

data_words=[word for (word,tag) in data]
data_tags=[tag for (word,tag) in data]
data=[] # for gc

wordsall=data_words[:8000]
bigramsall=[b for b in zip(wordsall[:-1],wordsall[1:])]
uniqbigrams=col.Counter(bigramsall) # bigrams only from given words, not added start and end boundaries
uniqwords=col.Counter(wordsall) # uniqwords from the set of first 8000 words

relevant_words=[w for w in data_words[:8000] if uniqwords[w]>=10]
word_class=[(w,w) for w in relevant_words] #initialization fo word-class map

classes=col.Counter(relevant_words) # initialization, starts with each word in its own class

#nize jeste nedorozmysleno
w10=[w for w in wordsall if uniqwords[w]>=10]
bi_class=col.Counter([(u,v) for (u,v) in uniqbigrams if uniqwords[u]>=10 and uniqwords[v]>=10])

#
#pp2ch=

N=len(wordsall)
print(sum([uniqbigrams[d,e]/(N-1)*math.log(uniqbigrams[d,e]*N*N/((N-1)*uniqwords[d]*uniqwords[e]),2)  for (d,e) in uniqbigrams]))
print(sum([uniqbigrams[d,e]/(N-1)*math.log(uniqbigrams[d,e]*N*N/((N-1)*uniqwords[d]*uniqwords[e]),2)  for (d,e) in uniqbigrams if (uniqwords[d]>=10 and uniqwords[e]>=10)]))

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

