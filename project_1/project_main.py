import urllib2
import json
import base64
import nltk
from nltk.corpus import stopwords
import string
from nltk import stem

def main():
  bingUrl = 'https://api.datamarket.azure.com/Bing/Search/Web?$format=json&Query=%27gates%27&$top=10'
  #Provide your account key here
  accountKey = 'aku05TIbEb+Glieu53ng1+Y7Y9kjjNjfNL3mUxJxQco'

  accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
  headers = {'Authorization': 'Basic ' + accountKeyEnc}
  req = urllib2.Request(bingUrl, headers = headers)
  response = urllib2.urlopen(req)
  content = response.read()
  data = json.loads(content)
  #content contains the xml/json response from Bing.
  positives = []
  negatives = []
  Query = 'Bill Gates'
  vocab = dict()
  q=10
  a=5
  b=1
  for word in preProcess(Query):
      vocab[word]=q
          
          
  #Take input from user
  for result in data['d']['results']:
      print '\nTitle:\n' + result['Title']
      print 'Description:\n'+ result['Description']
      flag = 0
      while flag==0:
          var = raw_input("Relevant or irrelevant(y/n)? :")
          if str(var)=='y':
              positives.append(result['Description'])
              for word in preProcess(result['Description']):
                  if word not in vocab.keys():
                      vocab[word]=a
                  else:
                      vocab[word]+=a
              flag = 1
          elif str(var)=='n':
              negatives.append(result['Description'])
              for word in preProcess(result['Description']):
                  if word not in vocab.keys():
                      vocab[word]=-b
                  else:
                      vocab[word]-=b
              flag = 1
          else:
              print 'Wrong Input. Enter again:'
  print 'precision = ', str(len(positives)*1.0/10)
  size_new = len(Query.split())+2
  print 'New Query :\n', sorted(vocab.keys(), key=vocab.get)[-size_new:]
  #print content

def preProcess(text):
    text=text.lower()
    stemmer=stem.PorterStemmer()
    for w in string.punctuation:
        text=text.replace(w,' ')
    words = text.split()
    words = [w for w in words if not w in stopwords.words('english')]
    #removed stemming for now
##    stemmed =[]
##    for w in words:
##      stemmed.append(stemmer.stem(w))  
    return words
    
if __name__ == '__main__':
  main()
