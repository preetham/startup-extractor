#! /usr/bin/env python3
# ~*~ utf-8 ~*~

import glob
import re

def preprocess(file_data):
    matches = re.split(r'<https://angel.co/today/stories/.*>', file_data, flags=re.MULTILINE)
    if matches is None:
        return
    i = 2
    articles = list()
    while i < len(matches) and len(matches) > 2:
        raw_article = matches[i]
        article = re.sub(r'\n', '', raw_article)
        article = re.sub(r'\*', '', article)
        article = re.sub('Join the discussion', '', article)
        articles.append(article)
        i = i + 3
    clean_article = '\n'.join(articles)
    return clean_article

def list_files(dir_path):
    file_list = glob.glob(dir_path)
    # file_list = ['./parsed-data/March 01, 2021.txt']
    return file_list

def read_file(path):
    with open(file=path, mode='r') as f:
        file_data = f.read()
        clean_data = preprocess(file_data=file_data)
        if clean_data and len(clean_data) > 0:
            file_name = path.split('/')[-1]
            with open('./clean-data/' + file_name, 'w') as wf:
                wf.write(clean_data)

files = list_files('./parsed-data/*.txt')
for file in files:
    read_file(file)
