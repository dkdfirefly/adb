import itertools

# Hardcoded samples
sample = [['pen', 'ink', 'diary', 'soap'], ['pen','ink', 'diary'],['pen','diary'], ['pen','ink','soap']]

# Input params
min_support = 0.7
min_conf = 0.8

# Terminologies
#   candGroup : list of list(candK) of list(cand) => The entire candidate structure
#   candK : list of list(cand) => candidate set of length K
#   cand : list => The actual candidate

# Initialisations
k=0
candGroup = []
candK = []
support = dict();

lineNum = 0
for rows in sample:
    lineNum += 1
    for item in rows:
        itemTuple = (item,)
        if itemTuple in support.keys():
            support[itemTuple].append(lineNum)
        else:
            support[itemTuple] = [lineNum]
print support
candK = [list(i) for i in support.keys() if (len(support[i])*1.0)/len(support.keys()) >= min_support];
candGroup.append(candK)
print 'group'
print candGroup
k+=1

candK = []

#join
for candInd1 in range(len(candGroup[k-1])):
    for candInd2 in range(candInd1+1, len(candGroup[k-1])):
        # check if all terms till the last one in cand match
        if candGroup[k-1][candInd1][:-1] == candGroup[k-1][candInd2][:-1]:
           temp = []
           # copy over the first cand from (k-1)
           temp.extend(candGroup[k-1][candInd1])
           # append the last term which is different
           temp.append(candGroup[k-1][candInd2][-1])
           candK.append(temp)
candGroup.append(candK)
print 'group'
print candGroup

#prune
candK = candGroup[-1]
candK_1 = candGroup[-2]
print 'candK'
print candK
print 'candK_1'
print candK_1
for cand in candK:
     # get all the permutations of cand
     for comb in list(itertools.combinations(cand,k)):
         print 'comb'
         print list(comb)
         # check if each permutation is present in the (k-1)
         if list(comb) not in candK_1:
             print 'in'
             if cand in candK:
                 candK.remove(cand)
                 print 'in2'

candGroup.pop()
candGroup.append(candK)

print 'group'
print candGroup
