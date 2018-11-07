pip install --user virtualenv &> /dev/null
mkdir env &> /dev/null
python -m virtualenv env -p /home/u1141153/python/bin/python3.5 &> /dev/null
source env/bin/activate.csh &> /dev/null
pip install spacy &> /dev/null
python -m spacy download en &> /dev/null
pip install -U scikit-learn &> /dev/null
python qa.py