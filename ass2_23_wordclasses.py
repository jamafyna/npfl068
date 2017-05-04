import sys
import collections as col
import icu
import math
import random
import datetime
import itertools

sin=sys.stdin
sout=sys.stdout 

SEPl="SEP["
SEPr="]SEP"
SEPi="SE,EP"


def getpartMI(a,b,c,N):
        """
        Compute one element of MI, only help function
        """
        return a*math.log(a*N/(b*c),2)

def getlossI(d,e):
        """
        Returns loss MI if d and e would be merged
        """
# s1 ... sum of new loss  MI of right neighbors if d, e  will be  merged
        s1=sum([getpartMI((bi_class[d,s]+bi_class[e,s]),(classes[d]+classes[e]),classes[s],N) for s in rightneib[d].union(rightneib[e]) if (s!=d and s!=e)])

        s1md=sum([getpartMI(bi_class[d,s],classes[d],classes[s],N) for s in rightneib[d] if s!=d])
         
        s1me=sum([getpartMI(bi_class[e,s],classes[e],classes[s],N) for s in rightneib[e] if s!=e])
# sum of loss MI of left neighbors of d, e if d and e will be merged
        s2=sum([getpartMI(bi_class[s,d]+bi_class[s,e],(classes[d]+classes[e]),classes[s],N) for s in leftneib[d].union(leftneib[e]) if (s!=d and s!=e)])

# s2md, s2mr ... previous elements (left neighbors of d and e) of MI, if d, e will be merged

        s2md=sum([getpartMI(bi_class[s,d],classes[d],classes[s],N) for s in leftneib[d] if s!=d])
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
                if minI>temp: 
                    minI=temp
                    c1=d
                    c2=e
        return (c1,c2,minI)

def mergetwoclasses(d,e,minI):
        """
        Do merge of two given classes, actualize all structures
        """
        #merge e into d
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
                    rightneib[l]=rightneib[l].union([d])
        for r in rightn: #remove e from leftneib[r], 
                if r!=d and r!=e and r in leftneib:
                     leftneib[r].remove(e)
                     leftneib[r]=leftneib[r].union([d])
        rightneib[d]=rightneibtemp
        leftneib[d]=leftneibtemp
        del leftneib[e] #možná není potřeba, časem ověřit
        del rightneib[e] #možná není potřeba, časem ověřit
        Hist.append("Minimal loss: "+str(minI)+"\t "+d+" \t"+e+" \t>\t "+d+" \t "+SEPl+" "+d+" "+SEPi+" "+e+" "+SEPr)
        classes_relevant.remove(e) 
        return 0

def processHistory(History,remClasses):
        """ Returns the another form of history --- the new class of classes a and b is named (a,b). If remClasses is given, returns also members of remaining classes.
        """
        for i in range(0,len(History)):
                h=History[i].split('\t')
                old=h[4] # item in History  has this form: ["Minloss"+'\t'+d+"\t"+e+"\t>\t"+d+"\t"+"("d+","+e")"], so h[4] is the more importent class (its name remains)
                new=h[5] # the name of the new class which should be used instead of one of names of the classes
                for j in range(i+1,len(History)):
                        temp=History[j]
                        History[j]=temp.replace(" "+h[4].strip()+" "," "+h[5].strip()+" ")
                for j in range(0,len(remClasses)): 
                    c=remClasses[j]# 
                    if (c.strip())==(h[4].strip()): 
                        remClasses[j]=h[5].strip()
        # the last substitution, only for classes
      
        for i in range(0,len(History)):
            t=History[i].split('\t')
            u5=t[5].replace(SEPl,"(").replace(SEPr,")").replace(SEPi,"+") # back to readable form
            u1=t[1].replace(SEPl,"(").replace(SEPr,")").replace(SEPi,"+") # back to readable form
            u2=t[2].replace(SEPl,"(").replace(SEPr,")").replace(SEPi,"+") # back to readable form
            #History[i]=t[0]+":\t"+u1+'\t'+u2+'\t'+'-->'+'\t'+u5
            History[i]=t[0]+":\t"+u5
        for i in range (0,len(remClasses)):
            d=remClasses[i]
            c=remClasses[i].replace(SEPr,")")
            c=c.replace(SEPl,"(")
            c=c.replace(SEPi,"+")
            d=d.replace(" ","")
            d=d.replace(SEPr,"")
            d=d.replace(SEPl,"")
            d=d.replace(SEPi," ")
            remClasses[i]=c+"\n\n"+d+"\n"
        return (History,remClasses)


def getI():
        return sum([bi_class[d,e]*math.log(bi_class[d,e]*N/(classes[d]*classes[e]),2) for (d,e) in bi_class])/N


# ---------------------- program --------------------------------------------

if(len(sys.argv)!=4 or (sys.argv[2]!="1" and sys.argv[2]!="2") or not sys.argv[3].isdigit()): 
    sys.exit('Not correct arguments, please run with 3 arguments: input-file, number (1=task with words, 2=task with tags), count of resulting classes (1 for full hierarchy).')
f=open(sys.argv[1],encoding="iso-8859-2",mode='rt')
task=sys.argv[2]
finalcount=int(sys.argv[3])
data=[l.split('/',1) for l in f.read().splitlines()]  # items in format: word,speech-tag which can contains '/'

data_words=[word for (word,tag) in data]
data_tags=[tag for (word,tag) in data]
data=[] # for gc


# ----------------------- initialization -----------------------------------

# data with start token
if task=="1": wordsall=["<start>"]+data_words[:8000]
else: wordsall=["<start>"]+data_tags
N=len(wordsall)-1
classes=col.Counter(wordsall) # initialization, starts with each word in its own class, all classes, includes also the not frequent oney

bi_class=col.Counter([b for b in zip(wordsall[:-1],wordsall[1:])]) # all bigrams of classes in data, with count of their occurancy

classes_relevant=[c for c in classes if classes[c]>=10] # classes_relevant...set of classes which can be merged (occures more than 10)

leftneib={} # left neighbors of a given class, hashtable
rightneib={} # right neighbors of a given class, hashtable
for c in classes_relevant: # can be also: for c in classes, but it is necessary
      leftneib[c]={a for (a,b) in bi_class if b==c}
      rightneib[c]={b for (a,b) in bi_class if a==c}

Hist=[] # array of history

# --------------------computation -------------------------------------------

I=getI()

while len(classes_relevant)>finalcount:
        (c1,c2,minloss)=getclassestomerge()
        mergetwoclasses(c1,c2,minloss)

# writing results to the file
if finalcount==1:f=open("results-23-all"+"-"+str(task)+"_"+sys.argv[1]+".txt",'wt')
else:f=open("results-23-"+str(finalcount)+"-"+str(task)+"_"+sys.argv[1]+".txt",'wt')

f.write("MI of the whole text: "+str(I)+"\n")
(History,Cl)=processHistory(Hist,classes_relevant)
f.write("HISTORY OF MERGING\n")
for i in range(0,len(History)): f.write('\nmerge'+(str(i+1))+"\n"+History[i]+'\n')
if finalcount!="1":
    f.write("\nFINAL CLASSES:\n")
    for i in range(0,len(Cl)): f.write("\nclass "+str(i+1)+":\n"+Cl[i])
f.close()


