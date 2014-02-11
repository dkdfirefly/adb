import urllib2
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
  #content contains the xml/json response from Bing. 
  print content

if __name__ == '__main__':
  main()

