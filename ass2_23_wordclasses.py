import sys
import collections as col
import icu
import math
import random
import datetime
import itertools

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
        #print(d,",",e," : ")
#sum of loss MI of right neighbors of d, e
        s1=sum([(bi_class[d,s]+bi_class[e,s])*math.log((bi_class[d,s]+bi_class[e,s])*N/((classes[d]+classes[e])*classes[s]),2)for s in set(rightneib[d]+rightneib[e]) if (s!=d and s!=e)])
        s1md=sum([(bi_class[d,s])*math.log((bi_class[d,s])*N/(classes[d]*classes[s]),2)for s in rightneib[d] if s!=d])
        s1me=sum([(bi_class[e,s])*math.log((bi_class[e,s])*N/(classes[e]*classes[s]),2) for s in rightneib[e] if s!=e])
         
#sum of loss MI of left neighbors of d, e
        s2=sum([(bi_class[s,d]+bi_class[s,e])*math.log((bi_class[s,d]+bi_class[s,e])*N/((classes[d]+classes[e])*classes[s]),2) for s in set(leftneib[d]+leftneib[e]) if (s!=d and s!=e)])
        s2md=sum([(bi_class[s,d])*math.log((bi_class[s,d])*N/(classes[d]*classes[s]),2) for s in leftneib[d] if s!=d])
        s2me=sum([(bi_class[s,e])*math.log(bi_class[s,e]*N/(classes[e]*classes[s]),2) for s in leftneib[e] if s!=e])

# due to s=d or s=e
        #  return sum([bi_class[d,e]*math.log(bi_class[d,e]*N/(classes[d]*classes[e]),2) for (d,e) in bi_class])/N

        caa=bi_class[e,e]+bi_class[e,d]+bi_class[d,e]+bi_class[d,d]
        if caa!=0:
                ca=classes[e]+classes[d]
                s3=caa*math.log((caa*N)/(ca**2),2)
        else:
                s3=0
        s3m=0
        if bi_class[d,d]!=0:
                s3m+=bi_class[d,d]*math.log(bi_class[d,d]*N/(classes[d]**2),2)
        if bi_class[e,e]!=0:
                s3m+=bi_class[e,e]*math.log(bi_class[e,e]*N/(classes[e]**2),2)

        return (-s1-s2-s3+s1me+s1md+s2me+s2md+s3m)/N
        

def getclassestomerge():
        c1=[]
        c2=[]
        minI=float("inf")
        for (d,e) in itertools.combinations(classes_relevant,2):
                temp=getlossI(d,e)
                if (d=="case" and e=='subject'):print("DEBUG:",d,e,temp) 
                if minI>temp: 
                    minI=temp
                    c1=d
                    c2=e
        print("DEBUG: minimal loss:",minI," classes: ",c1," ",c2)
        return (c1,c2)

def mergetwoclasses(d,e):
        #merge e into d
        print("DEBUG: d: ",d," e: ",e)
# merge bigrams of classes
        for l in leftneib[e]:
            if l!=e: 
                bi_class[l,d]+=bi_class[l,e]
        for r in rightneib[e]:
            if r!=e:bi_class[d,r]+=bi_class[e,r]
        bi_class[d,d]+=bi_class[e,e]
# merge classes counts
        classes[d]+=classes[e]
        rightneibtemp=list(set(rightneib[d]+rightneib[e]))
        if e in rightneibtemp:rightneibtemp.remove(e)

        #leftneibtemp=list(set(leftneib[d]+leftneib[e])^{e})
        #rightneibtemp=list(set(rightneib[d]+rightneib[e])^{e})
        leftneibtemp=list(set(leftneib[d]+leftneib[e]))
        if e in leftneibtemp: leftneibtemp.remove(e)
        leftn=leftneib[e].copy()
        rightn=rightneib[e].copy()
        for l in leftn: #remove e from rightneib[l], 
                if l!=d and l!=e and l in rightneib: 
                    if(e not in rightneib[l]):
                        print("DEBUG:ERROR, e not in rightneib, e:",e)
                    else: rightneib[l].remove(e) #the condition is necessary because words with count <10 can be neighbors of something but cannot have neighbors
                    if d not in rightneib[l]: rightneib[l]+=[d]

        for r in rightn: #remove e from leftneib[r], 
                if r!=d and r!=e and r in leftneib:
                     if e not in leftneib[r]:
                         print("!!!!!!!!!!!!!!!!!!!DEBUG,ERROR, e not in leftneib, e:",e)
                     else:leftneib[r].remove(e)
                     if d not in leftneib[r]: leftneib[r]+=[d]
                    # leftneib[r].union([d])
        rightneib[d]=rightneibtemp
        leftneib[d]=leftneibtemp
        del leftneib[e] #možná není potřeba, časem ověřit
        del rightneib[e] #možná není potřeba, časem ověřit
        Hist.append(d+"+"+e+"->"+d)
        print(d+"+"+e+"->"+d)
        classes_relevant.remove(e) 
        return 0

def getI():
        return sum([bi_class[d,e]*math.log(bi_class[d,e]*N/(classes[d]*classes[e]),2) for (d,e) in bi_class])/N



f=open(sys.argv[1],encoding="iso-8859-2",mode='rt')
data=[l.split('/',1) for l in f.read().splitlines()]  # items in format: word,speech-tag which can contains '/'
#for (word,tag) in data...

data_words=[word for (word,tag) in data]
data_tags=[tag for (word,tag) in data]
data=[] # for gc


# ----------------------- initialization -----------------------------------
#data with start token
wordsall=["<start>"]+data_words[:8000]
N=len(wordsall)-1
classes=col.Counter(wordsall) # initialization, starts with each word in its own class
bi_class=col.Counter([b for b in zip(wordsall[:-1],wordsall[1:])])
classes_relevant=[c for c in classes if classes[c]>=10]
leftneib={}
rightneib={}
#for c in classes_relevant:
for c in classes:
    leftneib[c]=[a for (a,b) in bi_class if b==c]
    rightneib[c]=[b for (a,b) in bi_class if a==c]


Hist=[] # array of history
#uniqwords=col.Counter(wordsall) # uniqwords from the set of first 8000 words

print(getI())
(c1,c2)=getclassestomerge()
mergetwoclasses(c1,c2)



while len(classes_relevant)>1:
        (c1,c2)=getclassestomerge()
        mergetwoclasses(c1,c2)
 
      #  print("MI:", getI())

# merge by správně měla zaměnit d za e, jinak chyba, protože se spravně nezaktualizuji sousede. Akorát, když se to udělá, tak hlásí r.64 domain math error

















# --------------------puvodne fungovalo
wordsall=["<start>"]+data_words[:8000]
bigramsall=[b for b in zip(wordsall[:-1],wordsall[1:])]
uniqbigrams=col.Counter(bigramsall) # bigrams only from given words, not added start and end boundaries
uniqwords=col.Counter(wordsall) # uniqwords from the set of first 8000 words
print(sum([uniqbigrams[d,e]/N*math.log(uniqbigrams[d,e]*N/(uniqwords[d]*uniqwords[e]),2)  for (d,e) in uniqbigrams]))

#---------------------------------------
#
#pp2ch=

N=len(wordsall)
print(sum([uniqbigrams[d,e]/(N-1)*math.log(uniqbigrams[d,e]*N*N/((N-1)*uniqwords[d]*uniqwords[e]),2)  for (d,e) in uniqbigrams]))
print(sum([uniqbigrams[d,e]/N*math.log(uniqbigrams[d,e]*N/(uniqwords[d]*uniqwords[e]),2)  for (d,e) in uniqbigrams]))
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

