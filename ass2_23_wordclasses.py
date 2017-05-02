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


# chytrá implementace:
def getmergedI(d,e,s):
        return
def getpartMI(a,b,c,N):
        return a*math.log(a*N/(b*c),2)

def getlossI(d,e):
        """
        Returns loss MI if d and e would be merged
        """
        #print(d,",",e," : ")
# s1 ... sum of new loss  MI of right neighbors if d, e  will be  merged
      #  s1=sum([(bi_class[d,s]+bi_class[e,s])*math.log((bi_class[d,s]+bi_class[e,s])*N/((classes[d]+classes[e])*classes[s]),2)for s in rightneib[d].union(rightneib[e]) if (s!=d and s!=e)])
        s1=sum([getpartMI((bi_class[d,s]+bi_class[e,s]),(classes[d]+classes[e]),classes[s],N) for s in rightneib[d].union(rightneib[e]) if (s!=d and s!=e)])

# s1md, s1mr ... previous elements (right neighbors of d and e) of MI, if d, e will be merged
        #s1md=sum([(bi_class[d,s])*math.log((bi_class[d,s])*N/(classes[d]*classes[s]),2)for s in rightneib[d] if s!=d])
        s1md=sum([getpartMI(bi_class[d,s],classes[d],classes[s],N) for s in rightneib[d] if s!=d])
       # s1me=sum([(bi_class[e,s])*math.log((bi_class[e,s])*N/(classes[e]*classes[s]),2) for s in rightneib[e] if s!=e])
         
        s1me=sum([getpartMI(bi_class[e,s],classes[e],classes[s],N) for s in rightneib[e] if s!=e])
# sum of loss MI of left neighbors of d, e if d and e will be merged
        #s2=sum([(bi_class[s,d]+bi_class[s,e])*math.log((bi_class[s,d]+bi_class[s,e])*N/((classes[d]+classes[e])*classes[s]),2) for s in leftneib[d].union(leftneib[e]) if (s!=d and s!=e)])
        s2=sum([getpartMI(bi_class[s,d]+bi_class[s,e],(classes[d]+classes[e]),classes[s],N) for s in leftneib[d].union(leftneib[e]) if (s!=d and s!=e)])

# s2md, s2mr ... previous elements (left neighbors of d and e) of MI, if d, e will be merged

        s2md=sum([getpartMI(bi_class[s,d],classes[d],classes[s],N) for s in leftneib[d] if s!=d])
       # s2me=sum([(bi_class[s,e])*math.log(bi_class[s,e]*N/(classes[e]*classes[s]),2) for s in leftneib[e] if s!=e])
        s2me=sum([getpartMI(bi_class[s,e],classes[e],classes[s],N) for s in leftneib[e] if s!=e])

        # due to s=d or s=e
        # s3 ...  the new part of MI
        caa=bi_class[e,e]+bi_class[e,d]+bi_class[d,e]+bi_class[d,d]
        if caa!=0:
                ca=classes[e]+classes[d]
                s3=caa*math.log((caa*N)/(ca**2),2)
        else:
                s3=0
        # s3m ... the old part of MI
        s3m=0
        if bi_class[d,d]!=0:
                s3m+=bi_class[d,d]*math.log(bi_class[d,d]*N/(classes[d]**2),2)
        if bi_class[e,e]!=0:
                s3m+=bi_class[e,e]*math.log(bi_class[e,e]*N/(classes[e]**2),2)

        return (-s1-s2-s3+s1me+s1md+s2me+s2md+s3m)/N
        

def getclassestomerge():
        """
        Returns 2 classes with minimal loss of MI, i.e. classes to merge
        """
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
        return (c1,c2,minI)

def mergetwoclasses(d,e,minI):
        """
        Do merge of two given classes, actualize all structures
        """
        #merge e into d
        print("DEBUG: d: ",d," e: ",e)
        # merge bigrams of classes
        # actualization of count of bigrams
        for l in leftneib[e]:
            if l!=e: 
                bi_class[l,d]+=bi_class[l,e]
        for r in rightneib[e]:
            if r!=e:bi_class[d,r]+=bi_class[e,r]
        bi_class[d,d]+=bi_class[e,e]
        # merge classes counts
        classes[d]+=classes[e]
        # remember the old neighbors of our two classes (due to changes in the next part)
        rightneibtemp=(rightneib[d].union(rightneib[e]))
        if e in rightneibtemp:rightneibtemp.remove(e)
        leftneibtemp=(leftneib[d].union(leftneib[e]))
        if e in leftneibtemp: leftneibtemp.remove(e)
        # actualization of neighbors of all items which are neighbors with e (e.g "rename" e to d in all items)
        leftn=leftneib[e].copy()
        rightn=rightneib[e].copy()
        for l in leftn: #remove e from rightneib[l], 
                if l!=d and l!=e and l in rightneib: 
                    rightneib[l].remove(e) #the condition is necessary because words with count <10 can be neighbors of something but cannot have neighbors
                    #if d not in rightneib[l]: rightneib[l]+=[d]
                    rightneib[l]=rightneib[l].union([d])
        for r in rightn: #remove e from leftneib[r], 
                if r!=d and r!=e and r in leftneib:
                     leftneib[r].remove(e)
                    # if d not in leftneib[r]: leftneib[r]+=[d]
                     leftneib[r]=leftneib[r].union([d])
        rightneib[d]=rightneibtemp
        leftneib[d]=leftneibtemp
        del leftneib[e] #možná není potřeba, časem ověřit
        del rightneib[e] #možná není potřeba, časem ověřit
        Hist.append("Minimal loss: "+str(minI)+"\t "+d+" \t"+e+" \t>\t "+d+" \t "+"( "+d+" , "+e+" )")
        print(d+"+"+e+"->"+d)
        classes_relevant.remove(e) 
        return 0

def processHistory(History,remClasses={}):
        """ Returns the another form of history --- the new class of classes a and b is named (a,b). If remClasses is given, returns also members of remaining classes.
        """
        for i in range(0,len(Hist)-1):
                h=History[i].split('\t')
                old=h[4] # item in History  has this form: [d+"\t"+e+"\t>\t"+d+"\t"+"("d+","+e")"], so h[4] is the more importent class (its name remains)
                old=h[5] # the name of the new class which should be used instead of one of names of the classes
                for j in range(i+1,len(Hist)):
                        temp=History[j]
                        History[j]=temp.replace(" "+h[4].strip()+" "," "+h[5].strip()+" ")
                for c in remClasses:
                    if c==h[4]: c=h[5]
        for i in range(0,len(History)):
            t=History[i].split('\t')
            History[i]=t[1]+'\t'+t[2]+'\t'+'-->'+'\t'+t[5]
            print(t[1]+'\t'+t[2]+'\t'+'-->'+'\t'+t[5])
        return (History,remClasses)


def getI():
        return sum([bi_class[d,e]*math.log(bi_class[d,e]*N/(classes[d]*classes[e]),2) for (d,e) in bi_class])/N
def doInitialization():
        # data with start token
        if task=="1": wordsall=["<start>"]+data_words[:8000]
        else:wordsall=["<start>"]+data_tags
        N=len(wordsall)-1
        classes=col.Counter(wordsall) # initialization, starts with each word in its own class
        bi_class=col.Counter([b for b in zip(wordsall[:-1],wordsall[1:])])
        if task=="1":classes_relevant=[c for c in classes if classes[c]>=10]
        else: classes_relevant=[c for c in classes if classes[c]>=5]

        leftneib={}
        rightneib={}
        for c in classes_relevant:
        #for c in classes:
                leftneib[c]={a for (a,b) in bi_class if b==c}
                rightneib[c]={b for (a,b) in bi_class if a==c}


        Hist=[] # array of history
        return

if(len(sys.argv)!=4 or (sys.argv[2]!="1" and sys.argv[2]!="2") or not sys.argv[3].isdigit()): 
    sys.exit('Not correct arguments, please run with 3 arguments: input-file, number (1=task with words, 2=task with tags), count of resulting classes (1 for full hierarchy).')
f=open(sys.argv[1],encoding="iso-8859-2",mode='rt')
task=sys.argv[2]
finalcount=int(sys.argv[3])
data=[l.split('/',1) for l in f.read().splitlines()]  # items in format: word,speech-tag which can contains '/'
#for (word,tag) in data...

data_words=[word for (word,tag) in data]
data_tags=[tag for (word,tag) in data]
data=[] # for gc


# ----------------------- initialization -----------------------------------
# global wordsall, N, classes, bi_class, classes_relevant, leftneib, rightneib, Hist
# doInitialization()
# because I couldnt use correctly global variables, there is the same text as in doInitialization

# data with start token
if task=="1": wordsall=["<start>"]+data_words[:8000]
else:wordsall=["<start>"]+data_tags
N=len(wordsall)-1
classes=col.Counter(wordsall) # initialization, starts with each word in its own class
bi_class=col.Counter([b for b in zip(wordsall[:-1],wordsall[1:])])
classes_relevant=[c for c in classes if classes[c]>=10]
leftneib={}
rightneib={}
for c in classes_relevant:
#for c in classes:
      leftneib[c]={a for (a,b) in bi_class if b==c}
      rightneib[c]={b for (a,b) in bi_class if a==c}

Hist=[] # array of history


print("MI of the whole text: ",getI())

while len(classes_relevant)>finalcount:
        (c1,c2,minloss)=getclassestomerge()
        mergetwoclasses(c1,c2,minloss)

# writing results to the file
if finalcount==1:f=open("results-23-all_"+sys.argv[1]+".txt",'wt')
else:f=open("results-23-"+str(finalcount)+"_"+sys.argv[1]+".txt",'wt')

(History,Cl)=processHistory(Hist,classes_relevant)
for h in History: f.write(h+'\n')
for c in Cl: print(c)

f.close()


