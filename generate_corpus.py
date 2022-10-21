# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 21:10:35 2022

load and explore general conference corpus

@author: Dylan
"""

from pathlib import Path
import os

path = 'C:/Users/Dylan/Datasets/lds/genconftext/'

# read contents of data folder
files = os.listdir(path)
files[0]

# create a list of talks
talks = []
for file in files:
    text = Path(path+file).read_text()
    talk = text[text.index('TEXT:')+7:]
    talks.append(talk)

# find avg length of talk (in chars)
avgs = [len(talk) for talk in talks]
avg = float(sum(avgs)/len(talks)) # 9964

# concatenate all talks together
corpus = ''
for file in files:
    text = Path(path+file).read_text()
    talk = text[text.index('TEXT:')+7:]
    corpus = corpus+talk
    
# find number of characters in corpus
len(corpus) # 40,025,220

# save corpus
Path(path+'gc_corpus.txt').write_text(corpus)
