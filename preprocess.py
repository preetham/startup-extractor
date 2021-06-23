#! /usr/bin/env python3
# ~*~ utf-8 ~*~

import glob
import re


def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

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
        article = re.sub(r'^\w+\s{1,3}', '', article)
        article = re.sub(r'^\w+\s{3}', '', article)
        article = re.sub(r'^\w+\s\w+\s{3}', '', article)
        raised = findWholeWord('raised')(article)
        series = re.search(r'Series\s[A,B,C,D,E]', article, flags=re.MULTILINE)
        if raised and series:
            articles.append(article.strip())
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
            with open('./raised-article-data/' + file_name, 'w') as wf:
                wf.write(clean_data)

files = list_files('./parsed-data/*.txt')
for file in files:
    read_file(file)
