import copy
import itertools
import operator
import sys

def apriori_join(candGroup,candK,k):
  """
    Perform join step of apriori
  """
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

def apriori_prune(candGroup,candK,k):
  """
    Perform prune step of apriori
  """
  #prune
  candK = copy.deepcopy(candGroup[-1])
  candK_1 = candGroup[-2]
  for cand in candK:
       # get all the permutations of cand
       for comb in list(itertools.combinations(cand,k)):
           # check if each permutation is present in the (k-1)
           if list(comb) not in candK_1:
               if cand in candGroup[-1]:
                   candGroup[-1].remove(cand)


def calcSupport(candK,candGroup,support,lineNum):
  """
    Calculate support for candidates
  """
  #support
  global loop
  loop= 0
  candK = copy.deepcopy(candGroup[-1])
  for cand in candK:
    set1 = set(support[tuple(sorted(cand[:-1]))])
    set2 = set(support[tuple(sorted([cand[-1]]))])
    setInt = set.intersection(set1, set2)
    if len(list(setInt))*1.0/lineNum < min_support:
      candGroup[-1].remove(cand)
    else:
      support[tuple(sorted(cand))] = list(setInt)
      loop = 1


def calcConf(candK,candGroup,support,conf,lineNum):
  """
    Calculate confidence for different permutations
  """
  #confidence
  global loop
  loop = 0
  candK = copy.deepcopy(candGroup[-1])
  for cand in candK:
    for perm in list(itertools.permutations(cand,len(cand))):
      for i in range(len(perm)-1):
        left = list(perm)[:(i+1)]
        right = list(perm)[(i+1):]
        confVal = len(support[tuple(sorted(cand))])*1.0/len(support[tuple(sorted(left))])
        suppVal = len(support[tuple(sorted(cand))])*100.0/lineNum
        if confVal >= min_conf:
          conf[(tuple(sorted(left)),tuple(sorted(right)))] = (confVal*100.0, suppVal)
          loop = 1

def printFreqItems(support,lineNum,outputFile):
  """
    Print the frequent itemsets with support higher than min_support
  """
  outputFile.write('==Frequent itemsets (min_sup=' + str(min_support*100.0) + '%)\n')
  for cand in sorted(support, key = lambda x: len(support[x]), reverse = True):
    outputFile.write(str(list(cand)) + ', ' + str(len(support[tuple(sorted(cand))])*100.0/lineNum) + '%\n')

def printHighConf(conf,outputFile):
  """
    Print rules with confidence higher than min_conf
  """
  outputFile.write('\n')
  outputFile.write('==High-confidence association rules (min_conf=' + str(min_conf*100.0) + '%)\n')
  for left, right in sorted(conf.items(), key=lambda (k, v): v[0], reverse = True):
    if len(list(left[1])) == 1:
      outputFile.write(str(list(left[0])) + ' => ' + str(list(left[1])) + ' (Conf: ' + str(right[0]) + '%, Supp: ' + str(right[1]) + '%)\n')

def processInput(fileName):
  """
    Process input dataset
  """
  sample = []
  file = open(fileName)
  i=0
  for line in file:
      i+=1
      line = line.strip('\n')
      temp = line.split(',')
      temp = filter(lambda a: a != '', temp)
      temp = filter(lambda a: a != '\n', temp)
      temp = filter(lambda a: a != 'N/A', temp)
      temp = filter(lambda a: a != ' ', temp)
      if len(temp)>7:
        sample.append(temp)
  return sample

def main(argv):
  """
    Get the freq itemsets and high conf association rules for provided dataset
  """

  global min_support
  global min_conf 

  if len(argv) != 4:
    print "Usage: python run.py INTEGRATED_DATASET.csv min_supp min_conf"
    sys.exit()

  # Input params
  sample = processInput(argv[1])
  outputFile = open("output.txt","w+")
  min_support = float(argv[2])
  min_conf = float(argv[3])

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

  # First iteration
  lineNum = 0
  for rows in sample:
      lineNum += 1
      for item in rows:
          itemTuple = (item,)
          if itemTuple in support.keys():
              support[itemTuple].append(lineNum)
          else:
              support[itemTuple] = [lineNum]

  candK = [list(i) for i in support.keys() if (len(support[i])*1.0)/lineNum >= min_support];
  candGroup.append(candK)
  sKeys = copy.deepcopy(support.keys())
  for key in sKeys:
    if len(support[key])*1.0/lineNum < min_support:
      support.pop(key)

  k+=1

  global loop
  loop = 1
  keyLength = support.keys()

  while k < keyLength and loop == 1:
    candK = []
    apriori_join(candGroup,candK,k)
    apriori_prune(candGroup,candK,k)
    calcSupport(candK,candGroup,support,lineNum)
    calcConf(candK,candGroup,support,conf,lineNum)
    k+= 1

  printFreqItems(support,lineNum,outputFile)  
  printHighConf(conf,outputFile)


"""
  Boilerplate syntax for calling main
"""
if __name__=='__main__':
  main(sys.argv)
