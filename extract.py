import spacy
import glob
from spacy import displacy
from collections import Counter
import en_core_web_sm
from pprint import pprint

nlp = en_core_web_sm.load()


def list_files(dir_path):
    file_list = glob.glob(dir_path)
    # file_list = ['./clean-data/March 01, 2021.txt']
    return file_list

def extract_entities(sentence):
    doc = nlp(sentence)
    pprint([(X.text, X.label_) for X in doc.ents])

def read_file(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            extract_entities(line)


files = list_files('./clean-data/*.txt')
for file in files:
    read_file(file)
