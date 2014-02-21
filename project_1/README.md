Requery
=========

Requery utilizes user relevance feedback to rephrase the initial query and thereby attempt to come up with better results.

It is a joint project by
  - Sarah Panda - sp3206
  - Dhaivat Shah - ds3267

    for the [Advanced Database Systems](http://www.cs.columbia.edu/~gravano/cs6111/) course

    Design Principle
    ----------------

    > The overriding design goal for the project
    > was to keep the code as readable and configurable as possible. 
    > While some complicated and to-say funky features
    > could be implemented, the implementation has been kept fairly general
    > so as not to favor particular types of queries and generate noise for
    > a whole lot other set.


    Essentials
    ----

    Bing account search key - **aku05TIbEb+Glieu53ng1+Y7Y9kjjNjfNL3mUxJxQco**

    The key is personal, and should not be used without contacting the author of this article.

    Installation
    --------------

    You need to install nltk in order to run the code.

    ```sh
    sudo pip install -U numpy
    sudo pip install -U pyyaml nltk
    ```
    These are the general instructions. Detailed instructions present at [nltk website](http://www.nltk.org/install.html)

    The above works only if you have sudo permission on your box. In case you don't, this is what can help:
    
    ```sh
    pip install --user numpy
    pip install --user pyyaml
    pip install --user nltk
    ```
    
    Also, you need to download specific corpus using nltk for use in this project. From the python prompt

    ```sh
    >>> import nltk
    >>> nltk.download("stopwords")
    ```
    You could alternatively use the windowed environment using just, if your system so provides
    ```sh
    >>> import nltk
    >>> nltk.download()
    ```
    Further information available in [nltk documentation](http://www.nltk.org/data.html)
    

    Usage
    -----------

    ```sh
    python project_main.py <account-key> <precision> <query>
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

    Features not provided for a purpose
    -------------------------
    - Considering the entire text from the url marked relevant: The user who marks the result relevant/irrelevant does not 
    see the entire page, so if we factor the entire content, that does not make lot of sense.
    - Authoritative websites: This would require a bit of network analysis to be done beforehand, which was not allowed for 
    this project; otherwise it would just be heuristics.
    - Stemming of words: As there are very few tokens that are considered at each iteration for query expansion, if different 
    tokens map to the same stemmed word, then it could add to the noise.
    
    
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
