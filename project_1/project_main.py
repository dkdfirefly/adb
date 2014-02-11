import urllib2
import json
import base64

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
  #Take input from user
  for result in data['d']['results']:
      print '\nTitle:\n' + result['Title']
      print 'Description:\n'+ result['Description']
      flag = 0
      while flag==0:
          var = raw_input("Relevant or irrelevant(y/n)? :")
          if str(var)=='y':
              positives.append(result['Description'])
              flag = 1
          elif str(var)=='n':
              negatives.append(result['Description'])
              flag = 1
          else:
              print 'Wrong Input. Enter again:'
  print 'precision = ', str(len(positives)*1.0/10)
  #print content

if __name__ == '__main__':
  main()
