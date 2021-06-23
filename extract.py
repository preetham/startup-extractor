import re
import spacy
import glob
from spacy import displacy
from collections import Counter
import en_core_web_sm
from pprint import pprint

nlp = en_core_web_sm.load()


def list_files(dir_path):
    file_list = glob.glob(dir_path)
    # file_list = ['./clean-dummy-data/April 26, 2021.txt']
    return file_list

def extract_entities(sentence):
    doc = nlp(sentence)
    orgs = list()
    money = list()
    series = re.search(r'Series\s[A,B,C,D,E]', sentence, flags=re.MULTILINE)
    if series:
        series = series[0]
    else:
        series = ''
    for token in doc.ents:
        if token.label_ == 'ORG' or token.label_ == 'NORP':
            orgs.append(token.text)
        if token.label_ == 'MONEY':
            money.append(token.text)
    for token in doc:
        if token.dep_ == 'nsubj' and token.i == 0:
            orgs.insert(0, token.text)
    return {
        'orgs': orgs,
        'money': money,
        'original_text': sentence.strip(),
        'round': series,
    }
    

def read_file(file_path):
    data = list()
    with open(file_path, 'r') as f:
        for line in f:
            entities = extract_entities(line)
            data.append(entities)
    return data

files = list_files('./raised-article-data/*.txt')
final_data = []
for file in files:
    final_data.extend(read_file(file))
import csv
with open('data.csv', 'w') as f:
    csvwriter = csv.writer(f, dialect='excel')
    csvwriter.writerow(['organisation', 'funding', 'round', 'original_text'])
    for d in final_data:
        org = ''
        money = ''
        if (d['orgs'] and len(d['orgs']) > 0):
            org = d['orgs'][0]
        if (d['money'] and len(d['money']) > 0):
            money = d['money'][0]
        if len(org) > 0 and len(money) > 0:
            data = [org, money, d['round'], d['original_text']]
            csvwriter.writerow(data)
