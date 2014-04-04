This is a text only version. To see the web version with better formatting, visit
https://github.com/dkdfirefly/adb/blob/master/project_2/README.md

which is coincidentally also where the project is hosted.
However, if for some reasons, you want to read plain txt only, carry on; there is no stopping you!


Knowledge Base
=========

Knowledge Base is a tool that queries Freebase database to give results in a structured format for user speified queries and answer simple questions, similar to how search engines these days work.

It is a joint project by
  - Sarah Panda - sp3206
  - Dhaivat Shah - ds3267

    for the [Advanced Database Systems](http://www.cs.columbia.edu/~gravano/cs6111/) course

Design Principle
----------------

 Freebase is a pool of structured information about various topics. 
 Our project uses Freebase API to get desired results in JSON format. Only a subset of all information
 is shown in the infobox, which is in accordance with the fields mentioned in the project description.
    
File List
----
- project_main.py - main source code
- mappings.txt - contains the fields taken into consideration for querying in case of infobox
- README.md - markdown syntax file
- README.txt - text version of README
- transcripts/infobox.txt - includes infobox for all queries given in the project description
- transcripts/question.txt - includes answers for all questions mentioned in the project description


Essentials
----

Freebase API key - **AIzaSyAa5--dD-33luOjnk6son8JqqkuHEQwKaQ**

The key is personal, and should not be used without contacting the author of this article.

Usage
-----------
    
No special package installations are required. The code has been tested on a local Linux machine as well as on the clic machine.

Any of the following formats would work:

python project_main.py --key <Freebase API key> -q <query> -t <infobox|question>
python project_main.py --key <Freebase API key> -f <file of queries> -t <infobox|question>
python project_main.py --key <Freebase API key>
    

Implementation
---------------
Part 1:
-------
    
The first section of the code, as well as the mappings.txt file specifies the fieldnames for different types of properties we wish to retrieve for a given query, with reference to the corresponding fields in the JSON results. This specification has 3 sections. 
  > First, we specify what categories we are going to look for (i.e. allowed results from within /type/object/type property). 
  > Second, we specify for each of the above mentioned categories, what are the properties we want to show.
  > Third defines an ordered dictionary of subproperties of the properties defined in the previous step, which are compound in nature.
    
When a user query is specified, first the query is passed to the Freebase search API. The results are sequentially traversed until at least one category of the topic in the result(also found using Freebase Search API) matches with our predefined set of allowed categories. 
    
For each of the category the result belongs to, the corresponding property values are extracted from the JSON output and printed in the infobox format.

**Note:**

  - We have grouped the properties by type, that is League-Team, League-Person and Person-Team properties are not mixed. However, all the person properties are grouped under a single header. The preference order is League followed by sports team and person at last
  - The data validity for each of the queried terms is done using try-catch statements checking for KeyError on return values.
  - A general framework is used for handling the printing for compound value types, based on compound values specified. This is a bit different from the reference implementation, but it made sense to have a general method, than to specify separately for all of them.
  - The ordering is maintained only at the level of the compound values and not for the property level.
    
Part 2:
-------
    
Questions in the form of 'Who created X?' are supported by this section. X could be either the name of a book or an organization, as only these two types are supported currently. The Freebase MQL read API is used to find the author/founder of the subject in the question. 
    
The specific fields used are:
    
  - /organization/organization_founder/organization_founded for BusinessPerson type of questions
  - /book/author/works_written for Author type of questions
    
**Note**
    
  - We have grouped author and business person type of results in case both of them are present for a particular person, unlike the reference implementation.
  - Sorting is by the name of the person in the alphabetical order.
    
    
Function description
---------------------
Though more detailed description is available in the code documentation, this is the brief idea.
    
  - **main** - check the input arguments and calls the appropriate functions
  - **getSubProp** - Fetches the subproperty values from the top level categories
  - **getSubPropValues** - Gets the specified value fields for both regular and compound properties, and handles their printing as well.
  - **getJSONResults** - This function handles forming the query URL and hits the Freebase search API to retrieve top JSON
  results.
  - **createInfoBox** -  handles infobox type of queries; after fetching the JSON results, gets the appropriate subproperty values.
  - **ansQues** -  handles the question answering part; queries the appropriate mql read api after getting the JSON results.
  - There are a few other helper function, but they are mainly for formatting issues and signal handling kind of stuff.
    
    
Error Handling
------------------
  We do not claim to have handled all the edge cases, but most of the common ones like argument errors, no matches found have been handled gracefully. As long as the queries are well formed and there are related results, there should not be an issue.
    

License
----

MIT


**Free Software, Hell Yeah!**
