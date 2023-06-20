# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 21:10:35 2022

load and explore general conference corpus

@author: Dylan
"""

from pathlib import Path
import os
from keras.preprocessing.text import Tokenizer

read_path = 'C:/Users/Dylan/Datasets/lds/genconftext/data/'
write_path = 'C:/Users/Dylan/Datasets/lds/genconftext/'

# read contents of data folder
files = os.listdir(read_path)
files[0]

# create a list of talks
talks = []
for file in files:
    text = Path(read_path+file).read_text()
    talk = text[text.index('TEXT:')+7:]
    talks.append(talk)

# find avg length of talk (in chars)
avgs = [len(talk) for talk in talks]
avg = float(sum(avgs)/len(talks)) # 9964

# concatenate all talks together
corpus = ''
for file in files:
    text = Path(read_path+file).read_text()
    talk = text[text.index('TEXT:')+7:]
    corpus = corpus+talk
    
# find number of characters in corpus
len(corpus) # 40,025,220

# save corpus
Path(write_path+'gc_corpus.txt').write_text(corpus)

# tokenize
t = Tokenizer()
t.fit_on_texts(talks)
print(t.word_counts)
print(t.document_count)
print(t.word_index)
print(t.word_docs)
