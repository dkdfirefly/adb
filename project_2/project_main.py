#!/usr/bin/env python
import urllib2
import json
import base64
import string
import sys

def getBingJSONResults(QueryTerms):
  Query = '%20'.join(QueryTerms)
  print Query
  Url = 'https://www.googleapis.com/freebase/v1/search?query=%27' + Query + '%27&key=AIzaSyAa5--dD-33luOjnk6son8JqqkuHEQwKaQ'
  print Url
  req = urllib2.Request(Url)
  response = urllib2.urlopen(req)
  content = response.read()
  data = json.loads(content)
  return data

QueryTerms = ['Bill','Gates']
data =  getBingJSONResults(QueryTerms)
for dt in data['result']:
    print dt['mid']
    print '--------------------'
    topicurl = 'https://www.googleapis.com/freebase/v1/topic'+str(dt['mid'])+'?key=AIzaSyAa5--dD-33luOjnk6son8JqqkuHEQwKaQ'
    print topicurl
    req = urllib2.Request(topicurl)
    response = urllib2.urlopen(req)
    content = response.read()
    detail = json.loads(content)
    print 'Done\n'
