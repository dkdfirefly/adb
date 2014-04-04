Knowledge Base
=========

Knowledge Base is a tool that queries Freebase database to give results in a structured format for user speified queries and answer simple questions, similar to how search engines these days work.

It is a joint project by
  - Sarah Panda - sp3206
  - Dhaivat Shah - ds3267

    for the [Advanced Database Systems](http://www.cs.columbia.edu/~gravano/cs6111/) course

    Design Principle
    ----------------

    > Freebase is a pool of structured information about various topics. 
    > Our project uses Freebase API to get desired results in JSON format. Only a subset of all information
    > is shown in the infobox, which is in accordance with the fields mentioned in the project description.
    
    File List
    ----
    - project_main.py - main source code
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
    
    Any of the following formats would work:
    
    ```sh
    python project_main.py --key <Freebase API key> -q <query> -t <infobox|question>
    python project_main.py --key <Freebase API key> -f <file of queries> -t <infobox|question>
    python project_main.py --key <Freebase API key>
    
    ```

    Implementation
    ---------------
    At the core of the project is the [rocchio relevance feedback mechanism](http://en.wikipedia.org/wiki/Rocchio_algorithm).
    
    However, the actual advantage comes from the tuning of the parameters. The default settings used are:
    - The tokens appearing in the documents marked relevant have been given five times the weightage as the diminishing factor
    aplied to tokens appearing in the irrelevant documents.
    - The tokens which are already present in the query formed thus far are ignored for all practical purposes.
    - Tokenisation is done on space separation and few of the punctuations have been removed.
    - The tokens appearing in the title are given more priority than those appearing in the descriptioon, as that is what 
    catches the eye of the user first.
    - The tokens present in query are not preprocessed at any point so as to allow any possible terms that the user may want
    in the query.
    - Reordering after query expansion is done based on high weights on bigrams collected from the relevant documents. Higher
    priority is given to bigrams than unigrams while deciding the order of terms in the new query sequence.
    
    
    Function description
    ---------------------
    Though more detailed description is available in the code documentation, this is the brief idea.
    
    - **main** - This function takes in arguments from command line and runs in loop until a specified precision level is achieved.
    The loop handles adding terms to the vocabulary, to keep count of frequency for both unigrams and bigrams. It performs 
    the query expansion wherein ordering is decided on the relative positioning of bigrams, if present, in relevant documents
    - **preProcess** - preProcess on any text, converts it into lowercase and removes punctuations(selected, ignoring a few like +, $)
    and stopwords.
    - **getBingJSONResults** - This function handles forming the query URL and hits the Bing Web search API to retrieve top 10 JSON
    results.
    - **addToVocab** - Given a text and a weight factor, this function adds the terms of the text and their respective weights to
    an existing vocabulary. 

    License
    ----

    MIT


    **Free Software, Hell Yeah!**
