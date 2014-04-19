import itertools
sample = [['pen', 'ink', 'diary', 'soap'], ['pen','ink', 'diary'],['pen','diary'], ['pen','ink','soap']]

L = []
k=0
min_support = 0.7
min_conf = 0.8

support = dict();
l0=[]
for rows in sample:
    for item in rows:
        try:
            support[item]+=1
        except KeyError:
            support[item]=1
print support
l0 = [[i] for i in support.keys() if (support[i]*1.0)/len(support.keys()) >= min_support];
L.append(l0)
k+=1

##### Candidate set #####
##l1=[]
##for i in range(len(L[k-1])):
##    for j in range(i+1,len(L[k-1])):
##        if L[k-1][i][:-1]==L[k-1][j][:-1]:
##           temp = []
##           temp.append(L[k-1][i])
##           temp[0].append(L[k-1][j][-1])
##           l1.append(temp)
##L.append(l1)
##print L

lnew=[]

#join
for i in range(len(L[k-1])):
    for j in range(i+1,len(L[k-1])):
        if L[k-1][i][:-1]==L[k-1][j][:-1]:
           temp = []
           temp.extend(L[k-1][i])
           temp.append(L[k-1][j][-1])
           lnew.append(temp)
L.append(lnew)

#prune
currentL = L[-1]
for candidate in currentL:
     for comb in list(itertools.combinations(candidate,1)):
         print list(set(comb))
##         if set(comb) not in L:
##             currentL.remove(candidate)
L = L[-1].extend(currentL)
print L
  
            

