#!/usr/bin/env python
import base64
import getopt
import json
import re
import signal
import string
import sys
import urllib2

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

def createInfoBox(query, apiKey):
  return 1

def ansQuestion(query, apiKey):
  return 1

def sigintHandler(signum, frame):
  """Handler function to safely exit on user pressing Ctrl+C
     Only for the case when using interactively.
  """
  sys.exit()

def printHelp():
  """Print the available Usage details
  """
  print 'project_main.py -key <Freebase API key> -q <query> -t <infobox|question>'
  print 'project_main.py -key <Freebase API key> -f <file of queries> -t <infobox|question>'
  print 'project_main.py -key <Freebase API key>'

def main(argv):
  """Check the input arguments and call appropriate functions
  """
  try:
    opts, args = getopt.getopt(argv,"f:hq:t:k:",["key="])
  except getopt.GetoptError:
    printHelp()
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      printHelp()
      sys.exit()
    elif opt == '-f':
      queryFile = arg
    elif opt == '-q':
      query = arg
    elif opt == '-t':
      task = arg
    elif opt in ("-k", "--key"):
      apiKey = arg

  notSpecified = [] # to contain the arguments which are not specified

  """
  'project_main.py -key <Freebase API key> -q <query> -t <infobox|question>' => target 1
  'project_main.py -key <Freebase API key> -f <file of queries> -t <infobox|question>' => target 2
  'project_main.py -key <Freebase API key>' => target 3
  """
  # Check if all the appropriate arguments have been specified
  try:
    apiKey
  except NameError:
    # key not specified
    printHelp()
    sys.exit()
  else:
    target = 3
  try:
    query # notSpecified index 1
  except NameError:
    notSpecified.append([1])
  else:
    try:
      task
    except NameError:
      # query specified but task not provided
      printHelp()
      sys.exit()
    else:
      target = 1
  try:
    queryFile # notSpecified index 2
  except NameError:
    notSpecified.append([2])
  else:
    try:
      task
    except NameError:
      # queryFile specified but task not provided
      printHelp()
      sys.exit()
    else:
      target = 2
  try:
    task # notSpecified index 3
  except NameError:
    notSpecified.append([3])
  else:
    try:
      query
    except NameError:
      try:
        queryFile
      except:
        # Neither query nor queryFile present but task specified
        printHelp()
        sys.exit()
      else:
        target = 2
    else:
      try:
        queryFile
      except NameError:
        target = 1
      else:
        # both query and queryFile present
        printHelp()
        sys.exit()
    if task not in ["infobox","question"]:
      printHelp()
      sys.exit()

  # Start processing based on type of request
  if(target == 1):
    # query specified
    if(task == "infobox"):
      createInfoBox(query, apiKey)
    elif(task == "question"):
      ansQuestion(query, apiKey)
  elif(target == 2):
    # queryFile specified
    f = open(queryFile, 'r')
    if(task == "infobox"):
      for line in f:
        createInfoBox(line.strip('\n'), apiKey)
    elif(task == "question"):
      for line in f:
        ansQuestion(line.strip('\n'), apiKey)
  elif(target == 3):
    # only key specified
    signal.signal(signal.SIGINT, sigintHandler)
    while(True):
      inputQuery =  raw_input(">>> ")
      if(inputQuery == ''):
        continue
      pat = 'Who created ([\w\s.-]+)\?*'
      match = re.search(pat, inputQuery, re.IGNORECASE)
      if match:
        query = match.group(1)
        ansQuestion(query, apiKey)
      else:
        query = inputQuery
        createInfoBox(query, apiKey)
  
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

# Boilerplate for calling main function
if __name__ == '__main__':
  main(sys.argv[1:])
