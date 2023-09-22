#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 17 16:59:40 2021

@author: anishagupta
"""

import numpy as np
import spacy

import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize, word_tokenize

import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

GLOVE_PATH = "content/glove.6B.50d.txt"   
DATA_PATH = "Datasets/harry_potter.txt"
GUESS = "Harry Potter"

def create_glove_dictionary(filename):
  glove_dict = {}
  with open(filename, 'r', encoding="utf-8") as f:
    for row in f:
      values = row.split()
      glove_dict[values[0]] = np.array([float(v) for i,v in enumerate(values) if i != 0])

  return glove_dict

def embed_glove_fn(tokens):
  embedding = []
  for token in tokens:
    if token.lower() in glove_dictionary:
      embedding.append(np.array(glove_dictionary[token.lower()]))

  return embedding

def preprocess_text(text, baseline=False):
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    if not baseline:
      text = text.lower()
      text = re.sub(r'\d+', '', text)
      text = text.translate(str.maketrans('','', string.punctuation))
    tokens = word_tokenize(text)
    if not baseline:
      preprocessed_tokens = []
      for t, tag in nltk.pos_tag(tokens):
        if t in stopwords.words("english"):
          continue
        if t in glove_dictionary:
          preprocessed_tokens.append(lemmatizer.lemmatize(t))
        else:
          preprocessed_tokens.append(t)
      tokens = preprocessed_tokens
    
    return tokens

def get_word_embeddings(text, embedding_reqd):
    x = embedding_reqd(text) # get elmo embedding of string (sentence-level)
    
    return x

def get_embeddings(sentences, embedding_reqd, baseline=False):
  data = []
  for review in sentences:
    tokens = preprocess_text(review, baseline=baseline)
    word_embeddings = get_word_embeddings(tokens, embedding_reqd)
    if len(word_embeddings) != 0:
        data.append(np.average(word_embeddings, axis=0))

  return data

def get_data_from_file(filename):
    with open(filename) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
        
    return lines

glove_dictionary = create_glove_dictionary(GLOVE_PATH)

sentences = get_data_from_file(DATA_PATH)
data = get_embeddings(sentences, embed_glove_fn, baseline=True)