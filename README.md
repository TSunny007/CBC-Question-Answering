# CBC-Question-Answering
Designing a question answering system to answer questions collected from the Canadian Broadcasting Corporation webpage for kids.

This program would take the input file path as a command line argument (The input.txt file is under testing folder). After running the instructions below, the output file will be writen under the testing folder.

## External Sources
* **spaCy** – https://spacy.io/
* **scikit-learn** – http://scikit-learn.org/stable/

## Estimated Running Time
* At most five minutes 

## Setting Up & Running The Application
### With a script file: 
(NOTE: If this script file does not work properly, please follow the direction to set it up without a script file below)

``./qa.sh``

### Without a script file: 
````
pip install --user virtualenv
mkdir env
python -m virtualenv env -p /home/u1141153/python/bin/python3.5
source env/bin/activate.csh
pip install spacy
python -m spacy download en
pip install -U scikit-learn
python qa.py testing/input.txt
````

## Other Information
* **CADE Lab Machine:** LAB2–29
* **Problems:** the shell script for installing spacy and scikit-learn does not work correctly all the time. So if that happens, please follow the instructions provided above.

## Scoring Result
````
FINAL RESULTS (developset)
AVERAGE RECALL =    0.4661  (234.93 / 504)
AVERAGE PRECISION = 0.3819  (147.78 / 387)
AVERAGE F-MEASURE = 0.4198

FINAL RESULTS (testset1)
AVERAGE RECALL =    0.4925  (154.17 / 313)
AVERAGE PRECISION = 0.4072  (98.95 / 243)
AVERAGE F-MEASURE = 0.4458
````


## Authors
* **Tarun Sunkaraneni** – load document files, format response file, find the best sentence list, and extract out the answer from the list of best sentence list
* **Mia Ngo** – write the README, write the shell script, set up the virtual machine environment for external applications, and extract out the answer from the list of best sentence list

