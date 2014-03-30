#!/usr/bin/env python
import urllib2
import json
import base64
from nltk.corpus import stopwords
from nltk import bigrams
import string
import sys
import collections
from collections import OrderedDict
import copy

global allcategories
global peopleProp
global detail
global compound

allcategories={'/people/person',
             '/book/author',
             '/film/actor',
             '/tv/tv_actor',
             '/organization/organization_founder',
             '/business/board_member',
             '/sports/sports_league',
             '/sports/sports_team',
             '/sports/professional_sports_team'}

#/people/person
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


def getBingJSONResults(QueryTerms):
  """Query Bing search API

  Space separates the query terms and queries the Bing search api to return data in JSON format
  """
  Query = '%20'.join(QueryTerms)
  #print Query
  Url = 'https://www.googleapis.com/freebase/v1/search?query=%27' + Query + '%27&key=AIzaSyAa5--dD-33luOjnk6son8JqqkuHEQwKaQ'
  #print Url
  req = urllib2.Request(Url)
  response = urllib2.urlopen(req)
  content = response.read()
  data = json.loads(content)
  return data

def getSubProp(prop):
  if prop=='/people/person' :
    getSubPropValues(peopleProp)
  elif prop =='/book/author' :
    getSubPropValues(authorProp)
  elif prop =='/film/actor' :
    getSubPropValues(actorProp)
  elif prop =='/tv/tv_actor':
    getSubPropValues(actorProp)
  elif prop =='/organization/organization_founder':
    getSubPropValues(boardMemberProp)
  elif prop =='/business/board_member':
    getSubPropValues(boardMemberProp)
  elif prop == '/sports/sports_league':
    getSubPropValues(leagueProp)
  elif prop == '/sports/sports_team':
    getSubPropValues(sportsTeamProp)
  elif prop =='/sports/professional_sports_team':
    getSubPropValues(sportsTeamProp)
  
def getSubPropValues(dictionary):
  #print dictionary
  val = dict();
  for k in dictionary.keys():
      print '\n@@@ ' + k
      param = dictionary[k]
      compound = copy.deepcopy(staticcompound)
      try:
        if detail["property"][param]["valuetype"] != 'compound':
          try:
            for records in detail["property"][param]["values"]:
              if param == "/common/topic/description":
                print records["value"]
              else:
                print records["text"]
          except KeyError:
            pass
        else:
            try:
              
              for allrecords in detail["property"][param]["values"]:
                 try:
                     compound = copy.deepcopy(staticcompound)
                     subprop = compound[param].popitem(last=True)
                    #for subprop in compound[param].keys():
                     try:
                      while subprop:
                       try:
                         for records in allrecords["property"][subprop[1]]["values"]:
                           sys.stdout.write(subprop[0] + '@'+ str(records["text"])+ ' ')
                       except KeyError:
                         pass
                       subprop = compound[param].popitem(last=True)
                     except KeyError:
                       pass
                 except KeyError:
                   pass
                 print
            except KeyError:
              pass
   
      except KeyError:
        pass
##    if k in detail["property"]:
##     val[k] = detail["property"][k]["values"][0]["text"]
##     print val[k]
  return val

##################################################################################
QueryTerms = ['Bill','Gates']
data =  getBingJSONResults(QueryTerms)
for topics in data['result']:
  dt = topics['mid']
  #print '--------------------'
  topicurl = 'https://www.googleapis.com/freebase/v1/topic'+str(dt)+'?key=AIzaSyAa5--dD-33luOjnk6son8JqqkuHEQwKaQ'
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

for types in  commonCategories:
  print '######## ' + str(types) + ' ########'
  getSubProp(types)
