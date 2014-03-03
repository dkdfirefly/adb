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
  req = urllib2.Request(bingUrl, headers = headers)
  response = urllib2.urlopen(req)
  content = response.read()
  data = json.loads(content)
  return data

def main():
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

    #content contains the xml/json response from Bing.
    data = getBingJSONResults(QueryTerms, headers)
    positives = []
    negatives = []
    vocab = dict()
    bigramdict = dict()
    
    q=10
    Title_factor = 1.5
    a=5
    b=1
 
    #Take input from user
    for result in data['d']['results']:
      title = result['Title'].encode('ascii','ignore')
      description = result['Description'].encode('ascii','ignore')
      print '\nTitle:\n' + title
      print 'Description:\n'+ description
      flag = 1
      while flag==1:
        var = raw_input("Relevant or irrelevant(y/n)? :")
        if str(var)=='y':
          positives.append(description)
          vocab = addToVocab(description, vocab, a,QueryTerms)
          vocab = addToVocab(title, vocab, a*Title_factor,QueryTerms)
          flag=0
        elif str(var)=='n':
          negatives.append(description)
          vocab = addToVocab(description, vocab, -b, QueryTerms)
          vocab = addToVocab(title, vocab, -b*Title_factor, QueryTerms)
          flag=0
        else:
          print 'Wrong Input. Enter again:'
          flag = 1
    current_precision = len(positives)*1.0/10
    print 'precision = ', str(current_precision)
    NewQuery=[]
    added =0
    for top in sorted(vocab.keys(), key=vocab.get)[-2:]:
      terms = top.split()
      if len(terms)==2 and terms[0] in QueryTerms and terms[1] in QueryTerms:
        if vocab[top] < vocab[''.join(reversed(terms))]:
          NewQuery.append(terms[1])
          NewQuery.append(terms[0])
        else:
          NewQuery.append(terms[0])
          NewQuery.append(terms[1])
        QueryTerms.remove(terms[0])
        QueryTerms.remove(terms[1])
      elif len(terms) ==2 and terms[0] not in QueryTerms:
        NewQuery.append(terms[0])
        NewQuery.append(terms[1])
        QueryTerms.remove(terms[1])
        added+=1
      elif len(terms) ==2 and terms[1] not in QueryTerms:
        NewQuery.append(terms[0])
        NewQuery.append(terms[1])
        QueryTerms.remove(terms[0])
        added+=1
      elif len(terms) ==2 and added==0:
        NewQuery.append(terms[0])
        NewQuery.append(terms[1])
        added += 2
      elif added!=2:
        NewQuery.append(top)
        added+=1
    print NewQuery   
    for new in NewQuery:
      QueryTerms.append(new.encode('ascii','ignore'))

    print 'New Query :\n', QueryTerms
    trial_num += 1

def addBigrams(text,factor,bigramdict):
  for word in bigrams(text):
            bi = ''.join(word)
            if bi not in bigramdict.keys():
              bigramdict[bi]=factor
            else:
              bigramdict[bi]+=factor
  return bigramdict

def addToVocab(text, Vocab, Rfactor, QueryTerms):
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
