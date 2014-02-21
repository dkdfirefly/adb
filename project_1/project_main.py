#!/usr/bin/env python
import urllib2
import json
import base64
from nltk.corpus import stopwords
from nltk import bigrams
import string
import sys

def getBingJSONResults(QueryTerms, headers):
  """Query Bing search API

  Space separates the query terms and queries the Bing search api to return data in JSON format
  """
  Query = '%20'.join(QueryTerms)
  bingUrl = 'https://api.datamarket.azure.com/Bing/Search/Web?$format=json&Query=%27' + Query + '%27&$top=10'
  print "URL: " + bingUrl
  req = urllib2.Request(bingUrl, headers = headers)
  response = urllib2.urlopen(req)
  content = response.read()
  data = json.loads(content)
  return data

def main():
  """
  Runs in loop till precision achieved.
  Does all the hard work !!
  The loop handles adding terms to the vocabulary, to keep count of frequency for both unigrams and bigrams. It performs the query expansion wherein ordering is decided on the relative 
  positioning of bigrams, if present, in relevant documents
  """
  if (len(sys.argv) == 4):
    accountKey = str(sys.argv[1])
    precision = float(sys.argv[2])
    Query = str(sys.argv[3])
  else:
    print 'Usage: ./project_main.py <account-key> <precision> <query>'
    sys.exit(2)

  QueryTerms = Query.lower().split()
  current_precision = 0.0
  trial_num = 0

  accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
  headers = {'Authorization': 'Basic ' + accountKeyEnc}

  while (current_precision < precision and current_precision != 0) or trial_num == 0:
    print "Parameters:"
    print "Client Key = " + accountKey
    print "Query  = " + ' '.join(QueryTerms)
    print "Precision  = " + str(precision)
    #content contains the xml/json response from Bing.
    data = getBingJSONResults(QueryTerms, headers)
    print "Total No of results  : 10"
    print "Bing Search Results:"
    print "==================="
    positives = []
    negatives = []
    vocab = dict()

    Title_factor = 1.5 # Additional priority give to title
    a=5 # weight for terms in relevant documents
    b=1 # weight for terms in irrelevant documents(negative)
 
    #Take input from user
    resultNum = 0
    for result in data['d']['results']:
      resultNum += 1
      print '\nResult ' + str(resultNum)
      print '==========='
      print 'Url:\n' + result['Url']
      print 'Title:\n' + result['Title']
      print 'Description:\n'+ result['Description']
      flag = 1
      while flag==1:
        var = raw_input("Relevant or irrelevant(y/n)? :")
        if str(var)=='y':
          positives.append(result['Description'])
          vocab = addToVocab(result['Description'], vocab, a,QueryTerms)
          vocab = addToVocab(result['Title'], vocab, a*Title_factor,QueryTerms)
          flag=0
        elif str(var)=='n':
          negatives.append(result['Description'])
          vocab = addToVocab(result['Description'], vocab, -b, QueryTerms)
          vocab = addToVocab(result['Title'], vocab, -b*Title_factor, QueryTerms)
          flag=0
        else:
          print 'Wrong Input. Enter again:'
          flag = 1
    NewQuery=[]
    added =0

    # Giving priority to bigram match
    topList = sorted(vocab.keys(), key=vocab.get)[-2:]
    if len(topList[1].split()) == 1:
      tmp = topList[1]
      topList[1] = topList[0]
      topList[0] = tmp

    # reordering query for optimisation
    # logic: (considering bigram presence in the relevant documents)
    #   possibilities
    #   1. if bigrams check for ordering the initial query too
    #   2. If just unigrams, add to the existing ones
    for top in reversed(topList):
      terms = top.split()
      # if both the bigram terms are already present in current query
      if len(terms)==2 and terms[0] in QueryTerms and terms[1] in QueryTerms:
        if (' '.join(reversed(terms))) in vocab.keys() and vocab[top] < vocab[' '.join(reversed(terms))]:
          NewQuery = appendC(NewQuery, terms[1])
          NewQuery = appendC(NewQuery, terms[0])
        else:
          NewQuery = appendC(NewQuery, terms[0])
          NewQuery = appendC(NewQuery, terms[1])
        QueryTerms.remove(terms[0])
        QueryTerms.remove(terms[1])
      # if one of the bigram terms is present in the current query
      elif len(terms) ==2 and terms[0] not in QueryTerms and terms[1] in QueryTerms:
        NewQuery = appendC(NewQuery, terms[0])
        NewQuery = appendC(NewQuery, terms[1])
        QueryTerms.remove(terms[1])
        added+=1
      elif len(terms) ==2 and terms[1] not in QueryTerms and terms[0] in QueryTerms:
        NewQuery = appendC(NewQuery, terms[0])
        NewQuery = appendC(NewQuery, terms[1])
        QueryTerms.remove(terms[0])
        added+=1
      # if none of the bigram terms are present in the current query
      elif len(terms) ==2 and added==0:
        NewQuery = appendC(NewQuery, terms[0])
        NewQuery = appendC(NewQuery, terms[1])
        added += 2
      # for unigrams
      elif added!=2:
        NewQuery = appendC(NewQuery, top)
        added+=1

    # Add the new query terms to the existing ones
    for new in NewQuery:
      QueryTerms.append(new.encode('ascii','ignore'))

    print '======================'
    print 'FEEDBACK SUMMARY'
    current_precision = len(positives)*1.0/10
    print 'Precision = ', str(current_precision)
    if current_precision < precision:
      print 'Still below the desired precision of ' + str(precision)
    else:
      print 'The required precision is reached'
    if current_precision != 0 and current_precision < precision:
      print 'New Query: ' + ' '.join(QueryTerms)
    elif current_precision == 0:
      print 'Zero precision reached. Exiting now!'

    trial_num += 1

def appendC(qList, term):
  """
  Append term only if not already present in qList
  """
  if qList == None:
    qList = []
  if len(qList) == 0 or term not in qList:
    qList.append(term)
  return qList    


def addBigrams(text,factor,bigramdict):
  """Add bigrams to the dictionary for terms in relevant documents
  """
  for word in bigrams(text):
    bi = ' '.join(word)
    if bi not in bigramdict.keys():
      bigramdict[bi]=factor
    else:
      bigramdict[bi]+=factor
  return bigramdict

def addToVocab(text, Vocab, Rfactor, QueryTerms):
  """
  Add terms to dictionary
  """
  for word in preProcess(text):
    if word not in Vocab.keys() and word not in QueryTerms:
      Vocab[word]=Rfactor
    elif word not in QueryTerms:
      Vocab[word]+=Rfactor
  Vocab = addBigrams(preProcess(text), Rfactor, Vocab)
  return Vocab
   
def preProcess(text):
  """Preprocess the given text

  All the text has been lower-cased.
  The stemmer has not been used currently, so as to avoid unrelated words mapping to the same terms which may add to the noise.
  A selective number of punctuations are removed to avoid removing punctuation that can be a part of the word.
  """
  text=text.lower()
  #original punctuation set
  #punc = ['!','"','#','$','%','&',"'",'(',')','*','+',',','-','.','/',':',';','<','=','>',';','?','@','[',"\\",']','^','_','`','{','|','}','~']
  punc = ['!','"','#','%',"'",'(',')','*',',','-','.','/',':',';','<','=','>',';','?','[',"\\",']','^','_','`','{','|','}','~']
  for w in punc:
    text=text.replace(w,' ')
  words = text.split()
  words = [w for w in words if not w in stopwords.words('english')] 
  return words
    
if __name__ == '__main__':
  main()
