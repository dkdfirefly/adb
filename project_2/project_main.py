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

allcategories={'/people/person',
             '/book/author',
             '/film/actor',
             '/tv/tv_actor',
             '/organization/organization_founder',
             '/business/board_member',
             '/sports/sports_league',
             '/sports/sports_team',
             '/sports/professional_sports_team'}

############################################

############## Category Prop ################

peopleProp = {'Name':'/type/object/name'
              ,'Birthday':"/people/person/date_of_birth"
              ,'PlaceofBirth':"/people/person/place_of_birth"
              ,'DeathPlace':"/people/deceased_person/cause_of_death"
              ,'DeathDate':"/people/deceased_person/date_of_death"
              ,'Siblings':"/people/person/sibling_s"
              ,'Description' : "/common/topic/description"
              ,'Spouses' : "/people/person/spouse_s"
              }

authorProp = { "Books": "/book/author/works_written",
	"BooksAboutTheAuthor": "/book/book_subject/works",
	"Influenced": "/influence/influence_node/influenced",
	"Influenced by": "/influence/influence_node/",
	}

actorProp = { "FilmsParticipated": "/film/actor/film", #compound
	}


leagueProp = {"Name": "/type/object/name",
	"Championship": "/sports/sports_league/championship",
	"Sport": "/sports/sports_league/sport",
	"Slogan": "/organization/organization/slogan",
	"OfficialWebsite": "/common/topic/official_website",
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
	   "PlayersRoster": "/sports/sports_team/roster", #compound
	}

boardMemberProp = {"Leadership": "/business/board_member/leader_of", #compound
		"BoardMember": "/business/board_member/organization_board_memberships", #compound
		"Founded": "/organization/organization_founder/organizations_founded",
	}

################ COMPOUND PROPERTIES ###################

staticcompound = {"/people/person/sibling_s":OrderedDict({"Sibling" : "/people/sibling_relationship/sibling"})
          ,"/business/board_member/organization_board_memberships" : OrderedDict({"From" : "/organization/organization_board_membership/from"
               ,"To" : "/organization/organization_board_membership/to"
               ,"Organization" : "/organization/organization_board_membership/organization"
               ,"Role" : "/organization/organization_board_membership/role"
               ,"Title" : "/organization/organization_board_membership/title"
              }),
           "/film/actor/film": OrderedDict({"FilmName": "/film/performance/film",
		"Character": "/film/performance/character",}),
	   "/sports/sports_league/teams": OrderedDict({"": "",
		}),
	   "/sports/sports_team/coaches": OrderedDict({"Name": "/sports/sports_team_coach_tenure/coach",
		"Position": "/sports/sports_team_coach_tenure/position",
		"From": "/sports/sports_team_coach_tenure/from",
		"To": "/sports/sports_team_coach_tenure/to",
		}),
	   "/sports/sports_team/league": OrderedDict({"": "",
		}),
	   "/sports/sports_team/roster": OrderedDict({"Name": "/sports/sports_team_roster/player",
		"Position": "/sports/sports_team_roster/position",
		"Number": "/sports/sports_team_roster/number",
		"From": "/sports/sports_team_roster/from",
		"To": "/sports/sports_team_roster/to",
		}),
            "/business/board_member/organization_board_memberships": OrderedDict({"From": "/organization/organization_board_membership/from",
		"To": "/organization/organization_board_membership/to",
		"Organization": "/organization/organization_board_membership/organization",
		"Role": "/organization/organization_board_membership/role",
		"Title": "/organization/organization_board_membership/title",
		}),
	   "/business/board_member/leader_of": OrderedDict({"From": "/organization/leadership/from",
		"To": "/organization/leadership/to",
		"Organization": "/organization/leadership/organization",
		"Role": "/organization/leadership/role",
		"Title": "/organization/leadership/title",
		}),
           "/people/person/spouse_s":OrderedDict({"Spouse":"/people/marriage/spouse"}),
           }

###################################
maxlen = 100
lindent = 20
subPropChecked = [0,0,0,0,0,0]

def reindent(s, numSpaces):
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
              subprop = compound[param].popitem(last=True)
              #for subprop in compound[param].keys():
              try:
                while subprop:
                  try:
                    for records in allrecords["property"][subprop[1]]["values"]:
                      if round == 0:
                        print '| ' + k + ':'
                        round = 1
                        print '|' + reindent('',lindent) + '|',
#                      sys.stdout.write(subprop[0] + '@'+ str(records["text"])+ ' ')
                      if len(str(records["text"])) > 18:
                        print (str(records["text"])[0:15] + '...' + '|').ljust(19),
                      else:
                        print (str(records["text"])).ljust(18) + '|',
                  except KeyError:
                    print ('').ljust(18) + '|',
                    pass
                  subprop = compound[param].popitem(last=True)
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
  data =  getBingJSONResults(query.split(' '),apiKey)
  for topics in data['result']:
    dt = topics['mid']
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
    commonCategories = set(categories).intersection(set(allcategories))
    if len(commonCategories)>0:
      print commonCategories
      break
  for i in range(0,5):
    subPropChecked[i] = 0
  for types in  commonCategories:
#    print '######## ' + str(types) + ' ########'
    getSubProp(types,detail)

def ansQuestion(query, apiKey):
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
	"type": "/people/person"
        }]

  queryBook = [{"/book/author/works_written": [{
		"a:name": None,
		"name~=": query
	}],
	"id": None,
	"name": None,
	"type": "/people/person"
        }]
  ######## Book or Organization? ###########
  dt = data['result'][0]['mid']
  topicurl = 'https://www.googleapis.com/freebase/v1/topic'+str(dt)+'?key=' + apiKey
  req = urllib2.Request(topicurl)
  response = urllib2.urlopen(req)
  content = response.read()
  detail = json.loads(content)
  categories = []
  for cg in detail['property']['/type/object/type']['values']:
    categories.append(cg['id'])
  print categories

  if '/organization/organization' in categories:
    queryNew = queryOrg
  elif '/book/book' in categories:
    queryNew = queryBook

############################################

  params = {
        'query': json.dumps(queryNew),
        'key': apiKey
  }
  service_url = 'https://www.googleapis.com/freebase/v1/mqlread'
  url = service_url + '?' + urllib.urlencode(params)
  response = json.loads(urllib.urlopen(url).read())

  for result in response['result']:
    print result['name']

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


# Boilerplate for calling main function
if __name__ == '__main__':
  main(sys.argv[1:])
