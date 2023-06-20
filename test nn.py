# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 19:55:02 2023

@author: Dylan
"""

import string
import re
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import glob
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
from tensorflow.keras.layers import Input, LSTM, Dense
from tensorflow.keras.models import Model


def preprocess_text(text_file):
    with open(text_file, 'r', encoding='utf-8') as f:
        text = f.read()

    # remove talk metadata
    text = text[text.index('TEXT:')+7:]
    
    # convert to lowercase
    text = text.lower()

    # remove digits and punctuations
    text = re.sub(f'[{string.punctuation}{string.digits}]', '', text)

    # remove extra whitespaces
    text = re.sub('\s+', ' ', text)

    # remove stop words
    stop_words = set(stopwords.words('english'))
    text = ' '.join(word for word in text.split() if word not in stop_words)

    # apply word stemming
    stemmer = SnowballStemmer('english')
    text = ' '.join(stemmer.stem(word) for word in text.split())

    return text


# set parameters
max_words = 10000
max_len = 100
latent_dim = 256

# create list of text files
text_files = glob.glob('C:/Users/Dylan/Datasets/lds/genconftext/data/*.txt')

# preprocess text files
texts = [preprocess_text(text_file) for text_file in text_files]

# fit tokenizer on preprocessed texts
tokenizer = Tokenizer(num_words=max_words, lower=True)
tokenizer.fit_on_texts(texts)

# convert preprocessed texts to sequences
sequences = tokenizer.texts_to_sequences(texts)

# pad sequences to have uniform length
sequences = pad_sequences(sequences, maxlen=max_len, padding='post', truncating='post')



# create input sequence
inputs = Input(shape=(max_len,4017))
x = LSTM(latent_dim)(inputs)
outputs = Dense(max_words, activation='softmax')(x)

# create model
model = Model(inputs=inputs, outputs=outputs)
model.compile(optimizer='adam', loss='categorical_crossentropy')

# fit model on preprocessed data
model.fit(sequences, np.roll(sequences, -1, axis=1), batch_size=32, epochs=100)


# sample function to generate text
def generate_text(model, tokenizer, seed_text, max_len, num_words):
    output_text = seed_text
    for i in range(num_words):
        # convert input sequence to numerical sequence
        input_seq = tokenizer.texts_to_sequences([output_text])[0]
        # pad input sequence to max length
        input_seq = np.pad(input_seq, (max_len - len(input_seq), 0), 'constant')
        # get next word probability distribution
        next_word_probs = model.predict(np.array([input_seq]))[0]
        # sample next word from distribution
        next_word_idx = np.random.choice(len(next_word_probs), p=next_word_probs)
        # convert index to word
        next_word = tokenizer.index_word[next_word_idx]
        # append next word to output text
        output_text += ' ' + next_word
    return output_text

# generate new text
generated_text = generate_text(model, tokenizer, seed_text, max_len, num_words)
print(generated_text)
