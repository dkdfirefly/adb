Association Rule Mining
=========

ARM is a tool that uses Apriori algorithm to find association rules from any given dataset.

It is a joint project by
  - Sarah Panda - sp3206
  - Dhaivat Shah - ds3267

    for the [Advanced Database Systems](http://www.cs.columbia.edu/~gravano/cs6111/) course

    Design Principle
    ----------------

    > The idea was to come up with interesting association rules using the NYC open datasets.
    > We have chosen the education field in particular and have tried to combine the demographic information
    > along with school progress and SAT results to derive these results.
    
    File List
    ----
    - run.py - main source code
    - final.csv - contains the INTEGRATED dataset in the csv format.
    - README.md - markdown syntax file
    - README.txt - text version of README
    - example-run.txt - Contains the output from an example run

    Usage
    -----------
    
    No special package installations are required. The code has been tested on a local Linux machine as well as on the clic machine.
    
    The commandline usage is as follows:
    
    ```sh
    python run.py INTEGRATED_DATASET.csv min_supp min_conf
    
    ```

    Implementation
    ---------------
    Dataset Generation:
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
    
    A-priori algorithm:
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
    
    - **apriori_join** - Perform join step of apriori
    - **apriori_prune** - Perform prune step of apriori
    - **calcConf** - Calculate confidence for different permutations
    - **calcSupport** - Calculate support for candidates
    - **main** - Get the freq itemsets and high conf association rules for provided dataset
    - **printFreqItems** - Print the frequent itemsets with support higher than min_support
    - **printHighConf** - Print rules with confidence higher than min_conf
    - **processInput** - Process input dataset

    
    Neglected Fields
    ------------------
    Blank Fields, those with only a space, a newline, fields with 'N/A' and those with field length lesser than threshold have been neglected for all purposes of this algorithm.
    

    License
    ----

    MIT


    **Free Software, Hell Yeah!**
