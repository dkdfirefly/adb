import copy
import itertools
import operator

# Hardcoded samples
#sample = [['pen', 'ink', 'diary', 'soap'], ['pen','ink', 'diary'],['pen','diary'], ['pen','ink','soap']]

sample = [['pen', 'ink', 'diary', 'soap','book'], ['pen','diary','ink','book'],['pen','ink','book'], ['pen','ink'], ['ink','soap','book'],['pen','ink','soap','book']]

# Input params
min_support = 0.5
min_conf = 0.6

# Terminologies
#   candGroup : list of list(candK) of list(cand) => The entire candidate structure
#   candK : list of list(cand) => candidate set of length K
#   cand : list => The actual candidate

# Initialisations
k=0
candGroup = []
candK = []
support = dict();
conf = dict();

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

candK = [list(i) for i in support.keys() if (len(support[i])*1.0)/lineNum >= min_support];
candGroup.append(candK)
sKeys = copy.deepcopy(support.keys())
for key in sKeys:
  if len(support[key])*1.0/lineNum < min_support:
    support.pop(key)

print support

print 'group'
print candGroup
k+=1

loop = 1
keyLength = support.keys()

while k < keyLength and loop == 1:
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
  candK = copy.deepcopy(candGroup[-1])
  candK_1 = candGroup[-2]
  for cand in candK:
       # get all the permutations of cand
       for comb in list(itertools.combinations(cand,k)):
           print 'comb'
           print list(comb)
           # check if each permutation is present in the (k-1)
           if list(comb) not in candK_1:
               print 'in'
               if cand in candGroup[-1]:
                   candGroup[-1].remove(cand)
                   print 'in2'

  print 'group'
  print candGroup

  #support
  loop = 0
  candK = copy.deepcopy(candGroup[-1])
  for cand in candK:
    print '------------- support ---------------'
    print cand
    set1 = set(support[tuple(sorted(cand[:-1]))])
    set2 = set(support[tuple(sorted([cand[-1]]))])
    setInt = set.intersection(set1, set2)
    print '------------- setint ----------------'
    print setInt
    if len(list(setInt))*1.0/lineNum < min_support:
      candGroup[-1].remove(cand)
    else:
      support[tuple(sorted(cand))] = list(setInt)
      loop = 1

  print support

  #confidence
  loop = 0
  candK = copy.deepcopy(candGroup[-1])
  for cand in candK:
    print cand
    for perm in list(itertools.permutations(cand,len(cand))):
      for i in range(len(perm)-1):
        left = list(perm)[:(i+1)]
        right = list(perm)[(i+1):]
        if len(support[tuple(sorted(cand))])*1.0/len(support[tuple(sorted(left))]) >= min_conf:
          conf[tuple(sorted(left))] = tuple(sorted(right))
          loop = 1
  print 'Problem solved'
  print conf

  k+= 1


# Result
#{('ink',): [1, 2, 4], ('pen',): [1, 2, 3, 4], ('pen', 'diary'): [1, 2, 3], ('ink', 'pen'): [1, 2, 4], ('diary',): [1, 2, 3]}
#{('ink',): ('pen',), ('diary',): ('pen',)}

print
print '==Frequent itemsets (min_sup=' + str(min_support*100.0) + '%)'
for cand in sorted(support, key = lambda x: len(support[x]), reverse = True):
  print str(list(cand)) + ', ' + str(len(support[tuple(sorted(cand))])*100.0/lineNum) + '%'

# TODO
#   print them in decreasing order of confidence
print
print '==High-confidence association rules (min_conf=' + str(min_conf*100.0) + '%)'
for left, right in conf.items():
  if tuple(sorted(tuple(left).__add__(tuple(right)))) in support.keys():
    print str(list(left)) + ' => ' + str(list(right)) + ' (Conf:' + str(len(support[tuple(sorted(tuple(left).__add__(tuple(right))))])*100.0/len(support[tuple(left)])) + '%, Supp: ' + str(len(support[tuple(cand)])*100.0/lineNum) + '%)'
  else:
    print str(list(left)) + ' => ' + str(list(right)) + ' (Conf:' + str(len(support[tuple(sorted(tuple(right).__add__(tuple(left))))])*100.0/len(support[tuple(left)])) + '%, Supp: ' + str(len(support[tuple(cand)])*100.0/lineNum) + '%)'


