Association Rule Mining
=========

ARM [(read here)](https://github.com/dkdfirefly/adb/blob/master/hw3/README.md) is a tool that uses Apriori algorithm to find association rules from any given dataset.

It is a joint project by
  - Sarah Panda - sp3206
  - Dhaivat Shah - ds3267

    for the [Advanced Database Systems](http://www.cs.columbia.edu/~gravano/cs6111/) course

    Design Principle
    ----------------

    > The idea was to come up with interesting association rules using the NYC open datasets.
    > We have chosen the education sector in particular and have tried to combine the demographic information
    > along with school progress and SAT results to derive these results. Datasets from two years have been used 
    > in order to demonstrate this relation.
    
    File List
    ----
    - run.py - main source code
    - INTEGRATED-DATASET.csv - contains the INTEGRATED dataset in the csv format.
    - README.md - markdown syntax file
    - README.txt - text version of README
    - example-run.txt - Contains the output from an example run
    - data/FINAL.db - sqlite db file which was used for integrating the datasets.

    Usage
    -----------
    
    No special package installations are required. The code has been tested on a local Linux machine as well as on the clic machine.
    
    The commandline usage is as follows:
    
    ```sh
    python run.py INTEGRATED-DATASET.csv min_supp min_conf
    ```

    Implementation
    ---------------
    Dataset Generation:
    -------
    
    In each of the datasets, we have used only those fields that are mentioned explicitly here. We have manipulated the numerical score values, so as to normalize them in a way to be conducive to the a-priori algorithm. Each of the division is an integral division, so as to bucketise the values. We have also  appended special characters in order to differentiate in between the numerical fields. Whenever a value was absent, it was replaced with a blank.
    
    ####SAT Results: [2010 data](https://data.cityofnewyork.us/Education/SAT-College-Board-2010-School-Level-Results/zt9s-n5aj) and [2012 data](https://data.cityofnewyork.us/Education/SAT-Results/f9bf-2cp4)

    ######Fields: SchoolID, readScore, MathScore, writeScore, year
  
    ######Particulars:
      - *schoolID* - initial 2 digits removed
      - *readscore* - value divided by 50, append "**-r**"
      - *mathScore* - value divided by 50, append "**-m**"
      - *writeScore* - value divided by 50, append "**-w**"
      - *year* - year of the dataset
    
    Appended the datasets from the two years together.

    ####Demographic: [data](https://data.cityofnewyork.us/Education/School-Demographics-and-Accountability-Snapshot-20/ihfw-zy9j)

    
    Filtered only years - 09-10, 11-12, in order to match with other datasets used.
    
    ######Fields: SchoolID, Asian-per, Black-per, Hispanic-per, White-per, Male-per, Female-per, year
    
    ######Particulars:
      - *schoolID* - initial 2 digits removed
      - *all others* - value divided by 10, append "**-a**"(asian), "**-b**"(black), "**-h**"(hispanic), "**-wh**"(white), "**-male**", "**-f**"(female)
      - *year* - as it is

    ####Progress Report: [data](https://data.cityofnewyork.us/Education/School-Progress-Report-Multi-year-2007-2011/5fsg-d8c9)

    Filtered only years: 2010-11, 2008-09, in order to match with other datasets used. Each record was broken down to 2 records - corresponding to each individual year.
    
    ######Fields: SchoolID, Grade, Year
    
    ######Particulars:
      - *schoolID* - as it is
      - *grade* - Grade for the following year
      - *year* - 201011 or 200809

    Dataset Integration:
    -------
    
    The objective was to compare the effect of a particular year's progress report on the following year's SAT scores and the effect of a school's demographic on the score distribution. In the process, we also obtained interesting rules for dependence of reading, writing and math scores in SAT on each other.

    **Join Steps:**
    
    - Left outer join of progress report with demographic based on schoolID and matching years. (*merge1*)
    - Left outer join of the *merge1* dataset with SAT results based on schoolID and for one year. (*merge2*)
    - Left outer join of the *merge2* dataset with SAT results based on schoolID and for another year. (*INTEGRATED_DATASET*)
    
    **Note:**
    
    SQLite was used for performing all the above operations and the associated .db file is also included along with the submission.
    

    A-priori algorithm:
    -------
    
    - The algorithm has been implemented exactly as mentioned in Section 2.1.1 of the paper - Rakesh Agrawal and Ramakrishnan Srikant: [Fast Algorithms for Mining Association Rules in Large Databases](http://www.cs.columbia.edu/~gravano/Qual/Papers/agrawal94.pdf), VLDB 1994.
    - Each of the following steps are executed in order: *join*, *prune*, thresholding by *min_support*, thresholding by *min_conf*.
    - This continues till the max size of the input record, or till when we have no more candidate sets.
    
    **Data Structures:**
    
    These are the main ones:
    
    - candGroup : list of list(candK) of list(cand) => The entire candidate structure
    - candK : list of list(cand) => candidate set of length K
    - cand : list => The actual candidate
    - support : Dictionary => Key: tuple of sorted cand, Value: list of intersected sets
    - conf : Dictionary => Key: tuple with sorted left and right association pair, Value: tuple of conf and support value.
    
    
    **Note**
    
    - *Neglected Fields* - Blank Fields, those with only a space, a newline, fields with 'N/A' and those with field length lesser than threshold have been neglected for all purposes of this algorithm.
    
    
    Sample Run:
    ------------

    This particular configuartion gives interesting results for this dataset.
    
    ```sh
    python run.py INTEGRATED-DATASET.csv 0.1 0.6
    ```

    We get association rules like:
    - ['7-r', 'B'] => ['7-w'] with (Conf: 92.6315789474%, Supp: 10.268378063%)
    - ['3-b', '7-r'] => ['7-w'] with (Conf: 91.6666666667%, Supp: 12.8354725788%)
    
    which has interpretations as :
    - schools with SAT reading scores from 350-400(7x50), and having grade 'B' tend to also have SAT writing scores from 350-400(7x50).
    - schools with 30-40%(3x10) black demographic and having reding scores from 350-400(7x50) also tend to have SAT writing scores from 350-400(7x50)
    - and so on.
    
    Thus we do get the relations we had set out to extract. There is a bit of bias for scores in the range 350-400 but that is because most of the results lie in that category.
    
    However, we do obtain associations mapping grades and demographic to results and the interdependence of SAT scores, which confirms our initial theory. As to why this particular combination, I would say because it gives about the right number of frequent itemsets and high conf association rules which can be comprehended and made sense of; as also explains the underlying truth for the dataset.
    

    
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

    
    

    License
    ----

    MIT


    **Free Software, Hell Yeah!**
