import urllib2
import json
import base64
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
import string
from nltk import stem
import sys

# Add steps to include nltk on clic - dhaivat
# TODO remove unused imports

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

  precision = 0.8
  Query = 'Candy skull'

  QueryTerms = Query.split()
  current_precision = 0.0
  trial_num = 0

  #Provide your account key here
  # TODO - Remove hard coding
  accountKey = 'aku05TIbEb+Glieu53ng1+Y7Y9kjjNjfNL3mUxJxQco'
  accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
  headers = {'Authorization': 'Basic ' + accountKeyEnc}

  while (current_precision < precision and current_precision != 0) or trial_num == 0:
    # the format and number of top results to be returned should come from config file
    data = getBingJSONResults(QueryTerms, headers)
    #content contains the xml/json response from Bing.
    positives = []
    negatives = []
    vocab = dict()
    # Weights need to come from an external config file
    q=10
    Title_factor = 1.5
    a=5
    b=1
    #for word in preProcess(Query):
    #  vocab[word]=q
          
    #Take input from user
    for result in data['d']['results']:
      print '\nTitle:\n' + result['Title']
      print 'Description:\n'+ result['Description']
      flag = 1
      while flag==1:
        var = raw_input("Relevant or irrelevant(y/n)? :")
        if str(var)=='y':
          positives.append(result['Description'])
          for word in preProcess(result['Description']):
            if word not in vocab.keys() and word not in QueryTerms:
              vocab[word]=a
            elif word not in QueryTerms:
              vocab[word]+=a
          for word in preProcess(result['Title']):
            if word not in vocab.keys() and word not in QueryTerms:
              vocab[word]=a*Title_factor
            elif word not in QueryTerms:
              vocab[word]+=a*Title_factor
          flag=0
        elif str(var)=='n':
          negatives.append(result['Description'])
          for word in preProcess(result['Title']):
            if word not in vocab.keys() and word not in QueryTerms:
              vocab[word]=-b*Title_factor
            elif word not in QueryTerms:
              vocab[word]-=b*Title_factor
          for word in preProcess(result['Description']):
            if word not in vocab.keys() and word not in QueryTerms:
              vocab[word]=-b
            elif word not in QueryTerms:
              vocab[word]-=b
          flag=0
        else:
          print 'Wrong Input. Enter again:'
          flag = 1
    current_precision = len(positives)*1.0/10
    print 'precision = ', str(current_precision)
    #size_new = len(Query.split('%20'))+2
    # Pick just two new relevant terms
    #TODO: use of authoritative sites
    #TODO: identify noisy words - dhaivat
    QueryTerms.extend(sorted(vocab.keys(), key=vocab.get)[-2:])
    print 'New Query :\n', QueryTerms
    trial_num += 1

  
def preProcess(text):
  """Preprocess the given text

  All the text has been lower-cased.
  The stemmer has not been used currently, so as to avoid unrelated words mapping to the same terms which may add to the noise.
  A selective number of punctuations are removed to avoid removing punctuation that can be a part of the word.
  """
  text=text.lower()
  stemmer=stem.PorterStemmer()
  #original punctuation set
  #punc = ['!','"','#','$','%','&',"'",'(',')','*','+',',','-','.','/',':',';','<','=','>',';','?','@','[',"\\",']','^','_','`','{','|','}','~']
  punc = ['!','"','#','%',"'",'(',')','*',',','-','.','/',':',';','<','=','>',';','?','[',"\\",']','^','_','`','{','|','}','~']
  for w in punc:
    text=text.replace(w,' ')
  words = text.split()
  words = [w for w in words if not w in stopwords.words('english')] 
  #TODO : punctuation list not to remove & + - sarah
  # TODO: remove unused code
  return words
    
if __name__ == '__main__':
  main()
