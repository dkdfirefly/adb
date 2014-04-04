#!/usr/bin/env python

import base64
from collections import OrderedDict
import copy
import getopt
import json
import re
import signal
import string
import sys
import textwrap
import urllib
import urllib2

allcategories={'/people/person':'',
             '/book/author':'AUTHOR',
             '/film/actor':'ACTOR',
             '/tv/tv_actor':'ACTOR',
             '/organization/organization_founder':'BUSINESS PERSON',
             '/business/board_member':'BUSINESS PERSON',
             '/sports/sports_league':'LEAGUE',
             '/sports/sports_team':'SPORTS TEAM',
             '/sports/professional_sports_team':'SPORTS TEAM'}

############################################

############## Category Prop ################

peopleProp = {'Name':'/type/object/name'
              ,'Birthday':"/people/person/date_of_birth"
              ,'Place of Birth':"/people/person/place_of_birth"
              ,'Death(Cause)':"/people/deceased_person/cause_of_death"
              ,'Death(Place)':"/people/deceased_person/place_of_death"
              ,'Death(Date)':"/people/deceased_person/date_of_death"
              ,'Siblings':"/people/person/sibling_s"
              ,'Description' : "/common/topic/description"
              ,'Spouses' : "/people/person/spouse_s"
              }

authorProp = { "Books": "/book/author/works_written",
	"Books About": "/book/book_subject/works",
	"Influenced": "/influence/influence_node/influenced",
	"Influenced by": "/influence/influence_node/influenced_by",
	}

actorProp = { "Films Participated": "/film/actor/film", #compound
	}


leagueProp = {"Name": "/type/object/name",
	"Championship": "/sports/sports_league/championship",
	"Sport": "/sports/sports_league/sport",
	"Slogan": "/organization/organization/slogan",
	"Official Website": "/common/topic/official_website",
	"Description": "/common/topic/description", #value
	"Teams": "/sports/sports_league/teams", #compound
	}

sportsTeamProp = {"Name": "/type/object/name",
                "Description": "/common/topic/description", #value
	   "Sport": "/sports/sports_team/sport",
	   "Arena": "/sports/sports_team/arena_stadium",
	   "Championships": "/sports/sports_team/championships",
	   "Coaches": "/sports/sports_team/coaches", #compound
	   "Founded": "/sports/sports_team/founded",
	   "Leagues": "/sports/sports_team/league", #compound
	   "Locations": "/sports/sports_team/location",
	   "Players Roster": "/sports/sports_team/roster", #compound
	}

boardMemberProp = {"Leadership": "/business/board_member/leader_of", #compound
		"BoardMember": "/business/board_member/organization_board_memberships", #compound
		"Founded": "/organization/organization_founder/organizations_founded",
	}

################ COMPOUND PROPERTIES ###################

staticcompound = {"/people/person/sibling_s":OrderedDict([("Sibling" , "/people/sibling_relationship/sibling")])
          ,"/business/board_member/organization_board_memberships" : OrderedDict([
               ("Organization", "/organization/organization_board_membership/organization")
               ,("Role" , "/organization/organization_board_membership/role")
               ,("Title" , "/organization/organization_board_membership/title")
               ,("From" , "/organization/organization_board_membership/from")
               ,("To" , "/organization/organization_board_membership/to")
              ]),
           "/film/actor/film": OrderedDict([
		("Character", "/film/performance/character"),
                ("FilmName", "/film/performance/film"),
                ]),
	   "/sports/sports_league/teams": OrderedDict([("TeamName", "/sports/sports_league_participation/team"),
		]),
	   "/sports/sports_team/coaches": OrderedDict([("Name", "/sports/sports_team_coach_tenure/coach"),
		("Position", "/sports/sports_team_coach_tenure/position"),
		("From", "/sports/sports_team_coach_tenure/from"),
		("To", "/sports/sports_team_coach_tenure/to"),
		]),
	   "/sports/sports_team/league": OrderedDict([("League Name", "/sports/sports_league_participation/league"),
		]),
	   "/sports/sports_team/roster": OrderedDict([("Name", "/sports/sports_team_roster/player"),
		("Position", "/sports/sports_team_roster/position"),
		("Number", "/sports/sports_team_roster/number"),
		("From", "/sports/sports_team_roster/from"),
		("To", "/sports/sports_team_roster/to"),
		]),
            "/business/board_member/organization_board_memberships": OrderedDict([
		("Organization", "/organization/organization_board_membership/organization"),
		("Role", "/organization/organization_board_membership/role"),
		("Title", "/organization/organization_board_membership/title"),
                ("From", "/organization/organization_board_membership/from"),
		("To", "/organization/organization_board_membership/to"),
		]),
	   "/business/board_member/leader_of": OrderedDict([
		("Organization", "/organization/leadership/organization"),
		("Role", "/organization/leadership/role"),
		("Title", "/organization/leadership/title"),
                ("From", "/organization/leadership/from"),
		("To", "/organization/leadership/to"),
		]),
           "/people/person/spouse_s":OrderedDict([("Name","/people/marriage/spouse"),
             ("From","/people/marriage/from"),
             ("To","/people/marriage/to"),
             ("Location","/people/marriage/location_of_ceremony"),
             ]),
           }

###################################
maxlen = 100
lindent = 20
subPropChecked = [0,0,0,0,0,0]

def reindent(s, numSpaces):
  """Indent the string s by numSpaces from the start
  """
  s = string.split(s, '\n')
  s = [(numSpaces * ' ') + string.lstrip(line) for line in s]
  s = string.join(s, '\n')
  return s

def chunks(l, n):
  """ Yield successive n-sized chunks from l.
  """
  for i in xrange(0, len(l), n):
    yield l[i:i+n]

def getSubProp(prop,detail):
  """
  Based on the top level categories found, fetches their corresponding subpropvalues
  """
  if prop=='/people/person' :
    if subPropChecked[0] == 0:
      getSubPropValues(peopleProp,detail)
    subPropChecked[0] = 1
  elif prop =='/book/author' :
    if subPropChecked[1] == 0:
      getSubPropValues(authorProp,detail)
    subPropChecked[1] = 1
  elif prop =='/film/actor' :
    if subPropChecked[2] == 0:
      getSubPropValues(actorProp,detail)
    subPropChecked[2] = 1
  elif prop =='/tv/tv_actor':
    if subPropChecked[2] == 0:
      getSubPropValues(actorProp,detail)
    subPropChecked[2] = 1
  elif prop =='/organization/organization_founder':
    if subPropChecked[3] == 0:
      getSubPropValues(boardMemberProp,detail)
    subPropChecked[3] = 1
  elif prop =='/business/board_member':
    if subPropChecked[3] == 0:
      getSubPropValues(boardMemberProp,detail)
    subPropChecked[3] = 1
  elif prop == '/sports/sports_league':
    if subPropChecked[4] == 0:
      getSubPropValues(leagueProp,detail)
    subPropChecked[4] = 1
  elif prop == '/sports/sports_team':
    if subPropChecked[5] == 0:
      getSubPropValues(sportsTeamProp,detail)
    subPropChecked[5] = 1
  elif prop =='/sports/professional_sports_team':
    if subPropChecked[5] == 0:
      getSubPropValues(sportsTeamProp,detail)
    subPropChecked[5] = 1
  
def getSubPropValues(dictionary,detail):
  """
  Gets the specified value fields for both the resgular and the compound properties.
  Handles printing each of them appropriately.
  """
  #print dictionary
  val = dict();
  for k in dictionary.keys():
    round = 0
    param = dictionary[k]
    compound = copy.deepcopy(staticcompound)
    try:
      if detail["property"][param]["valuetype"] != 'compound':
        try:
          for records in detail["property"][param]["values"]:
            if round == 0:
              print '| ' + k + ':',
              endPos = maxlen + lindent - 3 - len(k)
              print reindent('|',endPos)
              round = 1
            if param == "/common/topic/description":
              val = records["value"].replace('\n','')
              descValue = list(chunks(val,maxlen))
              for l in descValue:
                print '|' + reindent(l, lindent),
                endPos = maxlen - 1 - len(l)
                print reindent('|',endPos)
            else:
              textValue = list(chunks(records["text"],maxlen))
              for l in textValue:
                print '|' + reindent(l, lindent),
                endPos = maxlen - 1 - len(l)
                print reindent('|',endPos)
        except KeyError:
          pass
      else:
        try:
          for allrecords in detail["property"][param]["values"]:
            if round == 0:
              printCount = len(detail["property"][param]["values"])
            try:
              compound = copy.deepcopy(staticcompound)
              totalArg = len(compound[param])
              divLen = maxlen/totalArg
              subprop = compound[param].popitem(last=False)
              #for subprop in compound[param].keys():
              try:
                while subprop:
                  try:
                    rec = ''
                    for records in allrecords["property"][subprop[1]]["values"]:
                      if round == 0:
                        print '| ' + k + ':'
                        round = 1
                        print '|' + reindent('',lindent) + '|',
                        print subprop[0].ljust(divLen - 2) + '|',
                        for sub in compound[param]:
                          print sub.ljust(divLen - 2) + '|',
                        print
                        print '|' + reindent('',lindent),
                        print '-'* maxlen
                        print '|' + reindent('',lindent) + '|',
#                      sys.stdout.write(subprop[0] + '@'+ str(records["text"])+ ' ')
                      rec = rec +  records["text"] + ','
                    rec = rec[:-1]
                    if len(rec) > (divLen - 2):
                      print (rec[0:(divLen - 5)] + '...' + '|').ljust(divLen - 1),
                    else:
                      print (rec).ljust(divLen - 2) + '|',                    
                  except KeyError:
                    if round == 0:
                      print '| ' + k + ':'
                      round = 1
                      print '|' + reindent('',lindent) + '|',
                      print subprop[0].ljust(divLen - 2) + '|',
                      for sub in compound[param]:
                        print sub.ljust(divLen - 2) + '|',
                      print
                      print '|' + reindent('',lindent),
                      print '-'* maxlen
                      print '|' + reindent('',lindent) + '|',
                    print ('').ljust(divLen - 2) + '|',
                    pass
                  subprop = compound[param].popitem(last=False)
              except KeyError:
                pass
            except KeyError:
              pass
            print
            if printCount > 1:
              print '|' + reindent('',lindent) + '|',
              printCount = printCount - 1
        except KeyError:
          pass
   
    except KeyError:
      pass
##    if k in detail["property"]:
##     val[k] = detail["property"][k]["values"][0]["text"]
##     print val[k]
    else:
      print '-------------------------------------------------------------------------------------------------------------------------'
  return val


def getBingJSONResults(QueryTerms,apiKey):
  """Handles forming the query URL and hits the Freebase search API to retrieve the top JSON results
  """
  Query = '%20'.join(QueryTerms)
#  print Query
  Url = 'https://www.googleapis.com/freebase/v1/search?query=%27' + Query + '%27&key=' + apiKey
#  print Url
  req = urllib2.Request(Url)
  response = urllib2.urlopen(req)
  content = response.read()
  data = json.loads(content)
  return data

def createInfoBox(query, apiKey):
  """
  Handles the infobox types of queries
  Gets BING results, and calls getSubProp to get individual values
  """
  data =  getBingJSONResults(query.split(' '),apiKey)
  for topics in data['result']:
    dt = topics['mid']
    #print dt
    #print '--------------------'
    topicurl = 'https://www.googleapis.com/freebase/v1/topic'+str(dt)+'?key=' + apiKey
    #print topicurl
    req = urllib2.Request(topicurl)
    response = urllib2.urlopen(req)
    content = response.read()
    detail = json.loads(content)
    categories = []
    for cg in detail['property']['/type/object/type']['values']:
      categories.append(cg['id'])
    commonCategories = set(categories).intersection(set(allcategories.keys()))

    # Group by properties

    # Only league
    if "/sports/sports_league" in commonCategories:
      commonCategories = set(["/sports/sports_league"])
    # Only sports team
    elif "/sports/sports_team" in commonCategories:
      commonCategoies = set(["/sports/sports_team"])
    # Only professional sports team
    elif "/sports/professional_sports_team" in commonCategories:
      commonCategories = set(["/sports/professional_sports_team"])

    if len(commonCategories)>0:
      #print commonCategories
      break

  for i in range(0,6):
    subPropChecked[i] = 0
  categorynames = []
  try:
    for cat in commonCategories:
        categorynames.append(allcategories[cat])
    
    try:
       header = detail["property"]['/type/object/name']["values"][0]['text']+'('
    except KeyError:
        header = '('
    for cat in set(categorynames):
        if cat!='':
          header += cat+', '
    header = header[:-2]+')'
    print '-'*121
    print '|' + ' '*((119 - len(header))/2) + header + ' '*((119 - len(header))/2) + ' |'
    print '-'*121
    for types in  commonCategories:
  #    print '######## ' + str(types) + ' ########'
      getSubProp(types,detail)
  except:
    print 'No matches found....Exiting'
    sys.exit()

def ansQuestion(query, apiKey):
  """
  Handles the question answering part of the query
  Gets the BING results, and creates the MQL query fetching appropriate results
  """
  QueryTerms = query.split(' ')
  data =  getBingJSONResults(QueryTerms, apiKey)
  ############## Query Types ###############
  queryOrg = [{
	"/organization/organization_founder/organizations_founded": [{
		"a:name": None,
		"name~=": query
	}],
	"id": None,
	"name": None,
	"type": "/organization/organization_founder"
        }]

  queryBook = [{"/book/author/works_written": [{
		"a:name": None,
		"name~=": query
	}],
	"id": None,
	"name": None,
	"type": "/book/author"
        }]
  resultDict = {}
  ######## Book or Organization? ###########
  try:
   dt = data['result'][0]['mid']
  except:
    print 'No matches found.....Exiting'
    sys.exit()
  topicurl = 'https://www.googleapis.com/freebase/v1/topic'+str(dt)+'?key=' + apiKey
  req = urllib2.Request(topicurl)
  response = urllib2.urlopen(req)
  content = response.read()
  detail = json.loads(content)
  categories = []
  for cg in detail['property']['/type/object/type']['values']:
    categories.append(cg['id'])
#  print categories

  if '/organization/organization' or '/organization/organization_founder' in categories:
    queryNew = queryOrg
    params = {
          'query': json.dumps(queryNew),
          'key': apiKey
    }
    service_url = 'https://www.googleapis.com/freebase/v1/mqlread'
    url = service_url + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())

    for result in response['result']:
      resultDict[result["name"]] = "(as BusinessPerson) created "
      for org in result['/organization/organization_founder/organizations_founded']:
        resultDict[result["name"]] += '<' + org['a:name'] + '>' + ', '
#      print result['name']

  if '/book/author' or '/book/book' in categories:
    queryNew = queryBook
    params = {
          'query': json.dumps(queryNew),
          'key': apiKey
    }
    service_url = 'https://www.googleapis.com/freebase/v1/mqlread'
    url = service_url + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())

    for result in response['result']:
      if result["name"] in resultDict.keys():
        resultDict[result["name"]] += "and (as Author) created "
      else:
        resultDict[result["name"]] = "(as Author) created "
      for book in result['/book/author/works_written']:
        resultDict[result["name"]] += '<' + book['a:name'] + '>' + ', '
#    print result['name']

  count = 1
  for key in sorted(resultDict.keys()):
    print str(count) + '. ' + key + ' ' + resultDict[key][:-2]
    count += 1

def sigintHandler(signum, frame):
  """Handler function to safely exit on user pressing Ctrl+C
      Only for the case when using interactively.
  """
  sys.exit()

def printHelp():
  """Print the available Usage details
  """
  print 'project_main.py --key <Freebase API key> -q <query> -t <infobox|question>'
  print 'project_main.py --key <Freebase API key> -f <file of queries> -t <infobox|question>'
  print 'project_main.py --key <Freebase API key>'
  print '***************************************************************************'
  print "Please Note: There are two hyphen for key argument (See above for usage)"
  print '***************************************************************************'

def main(argv):
  """Check the input arguments and call appropriate functions
  """
  try:
    opts, args = getopt.getopt(argv,"f:hq:t:",["key="])
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
    elif opt == "--key":
      apiKey = arg

  notSpecified = [] # to contain the arguments which are not specified

  """
  'project_main.py --key <Freebase API key> -q <query> -t <infobox|question>' => target 1
  'project_main.py --key <Freebase API key> -f <file of queries> -t <infobox|question>' => target 2
  'project_main.py --key <Freebase API key>' => target 3
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
      print 'Query: ' + query
      print
      createInfoBox(query, apiKey)
    elif(task == "question"):
      print 'Question: ' + query
      print
      pat = 'Who created ([\w\s.-]+)\?*'
      match = re.search(pat, query, re.IGNORECASE)
      if match:
        query = match.group(1)
        ansQuestion(query, apiKey)
  elif(target == 2):
    # queryFile specified
    f = open(queryFile, 'r')
    if(task == "infobox"):
      for line in f:
        print 'Query: ' + line
        createInfoBox(line.strip('\n'), apiKey)
        print
    elif(task == "question"):
      for line in f:
        print 'Question: ' + line
        pat = 'Who created ([\w\s.-]+)\?*'
        match = re.search(pat, line.strip('\n'), re.IGNORECASE)
        if match:
          query = match.group(1)
          ansQuestion(query, apiKey)
        print
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
        print 'Question: ' + inputQuery
        print
        ansQuestion(query, apiKey)
      else:
        query = inputQuery
        print 'Query: ' + inputQuery
        print
        createInfoBox(query, apiKey)


# Boilerplate for calling main function
if __name__ == '__main__':
  main(sys.argv[1:])

