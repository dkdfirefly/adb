Requery
=========

Requery utilizes user relevance feedback to rephrase the initial query and thereby attempt to come up with better results.

It is a joint project by
  - Sarah Panda - sp3206
    - Dhaivat Shah - ds3267

    for the [Advanced Database Systems] course

    Design Principle
    ----------------

    > The overriding design goal for the project
    > was to keep the code as readable and configurable as possible. 
    > The idea is to provide all the modifiable parameters
    > in a separate xml file and hence they can be used to suit one's 
    > needs. While some complicated and to-say funky features
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
    These are the general instructions. Detailed instructions present at [nltk website]

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
    Further information available in [nltk documentation]


    Usage
    -----------

    ```sh
    python project_main.py <account-key> <precision> <query>
    ```

    Implementation
    ---------------
    At the core of the project is the [rocchio relevance feedback mechanism].

    However, the actual advantage comes from the tuning of the parameters. The default settings used are:
    - The tokens appearing in the documents marked relevant have been given five times the weightage as the diminishing factor aplied to tokens appearing in the irrelevant documents.
    - The tokens which are already present in the query formed thus far are ignored for all practical purposes.
    - Tokenisation is done on space separation and few of the punctuations have been removed.
    - The tokens appearing in the title are given more priority than those appearing in the descriptioon, as that is what catches the eye of the user first.
    - The tokens present from responses which are from authoritative websites (list to follow) are given higher weightage.


    ### Function description
    Though more detailed description is available in the code documentation, this is the brief idea.

    * **main** - 
    * **preProcess** - 
    * **getBingJSONResults** - 


    License
    ----

    MIT


    **Free Software, Hell Yeah!**

    [nltk website]:http://www.nltk.org/install.html
    [Advanced Database Systems]:http://www.cs.columbia.edu/~gravano/cs6111/
    [nltk documentation]:http://www.nltk.org/data.html
    [rocchio relevance feedback mechanism]:http://en.wikipedia.org/wiki/Rocchio_algorithm