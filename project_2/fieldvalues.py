#!/usr/bin/env python
import urllib2
import json
import base64
from nltk.corpus import stopwords
from nltk import bigrams
import string
import sys
from collections import defaultdict
global allcategories
global peopleProp
global detail

###################################

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
	"Slogan": "/organization/organization/slogan"",
	"OfficialWebsite": "/common/topic/official_website",
	"Description": "/common/topic/description", #value
	"Teams": "/sports/sports_league/teams", #compound
	}

sportTeamProp = {"Name": "/type/object/name",
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
tvactorProp = {}

################ COMPOUND PROPERTIES ###################

Sibling = {"/people/person/sibling_s":{"Sibling" : "/people/sibling_relationship/sibling"}
          ,"/business/board_member/organization_board_memberships" : {"From" : "/organization/organization_board_membership/from"
               ,"To" : "/organization/organization_board_membership/to"
               ,"Organization" : "/organization/organization_board_membership/organization"
               ,"Role" : "/organization/organization_board_membership/role"
               ,"Title" : "/organization/organization_board_membership/title"
              }
           }

###################################




def getBingJSONResults(QueryTerms):
  """Query Bing search API

  Space separates the query terms and queries the Bing search api to return data in JSON format
  """
  Query = '%20'.join(QueryTerms)
  print Query
  Url = 'https://www.googleapis.com/freebase/v1/search?query=%27' + Query + '%27&key=AIzaSyAa5--dD-33luOjnk6son8JqqkuHEQwKaQ'
  print Url
  req = urllib2.Request(Url)
  response = urllib2.urlopen(req)
  content = response.read()
  data = json.loads(content)
  return data

def getSubProp(prop):
  if prop=='/people/person' :
    getSubPropValues(peopleProp)
  elif prop =='/book/author' :
    getSubPropValues(peopleProp)
  elif prop =='/film/actor' :
    getSubPropValues(peopleProp)
  elif prop =='/tv/tv_actor':
    getSubPropValues(peopleProp)
  elif prop =='/organization/organization_founder':
    getSubPropValues(peopleProp)
  elif prop =='/business/board_member':
    getSubPropValues(peopleProp)
  elif prop == '/sports/sports_league':
    getSubPropValues(peopleProp)
  elif prop == '/sports/sports_team':
    getSubPropValues(peopleProp)
  elif prop =='/sports/professional_sports_team':
    getSubPropValues(peopleProp)
  
def getSubPropValues(dictionary):
  print dictionary
  val = dict();
  for k in dictionary.keys():
      param = dictionary[k]
      if detail["property"]["valuetype"] != 'compound':
        try:
         print detail["property"][param]["values"][0]["text"]
        except KeyError: pass
      else:
        for subprop in compound[param]:
          try:
             print detail["property"][param]["property"][subprop]["values"][0]["text"]
          except KeyError: pass

##    if k in detail["property"]:
##     val[k] = detail["property"][k]["values"][0]["text"]
##     print val[k]
  return val

##################################################################################
QueryTerms = ['Bill','Gates']
data =  getBingJSONResults(QueryTerms)
dt = data['result'][0]['mid']
print '--------------------'
topicurl = 'https://www.googleapis.com/freebase/v1/topic'+str(dt)+'?key=AIzaSyAa5--dD-33luOjnk6son8JqqkuHEQwKaQ'
print topicurl
req = urllib2.Request(topicurl)
response = urllib2.urlopen(req)
content = response.read()
detail = json.loads(content)
##try:
##  detail["property"]['/type/object/name']['value'][0]['text']
##except KeyError: print detail["property"]['/type/object/name']['values'][0]['text']
##categories = []
##for cg in detail['property']['/type/object/type']['values']:
##  categories.append(cg['id'])
print 'Original .... ' + str(detail["property"]["/people/person/date_of_birth"]["values"][0]["text"])
print getSubProp('/people/person')
