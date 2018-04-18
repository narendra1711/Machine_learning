# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 19:16:51 2018

@author: narendra
"""

import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

from nltk.corpus import brown
brown.words()

nltk.set_proxy('http://proxy.example.com:3128', ('USERNAME', 'PASSWORD'))
nltk.download()

stopwords.words('english')[:16]

para = "The program was open to all women between the ages of 17 and 35, in good health, who had graduated from an accredited high school. "
words = word_tokenize(para)
print(words)

#These are the words of one sentence. Let’s see if we can remove the stop words:
useful_words = [word for word in words if word not in stopwords.words('english')]
print(useful_words)

movie_reviews.words()
movie_reviews.categories()
movie_reviews.fileids()[:4]

#We can create a frequency distribution of the words, which will allow us to see which words are the most common in our reviews
all_words = movie_reviews.words()
freq_dist = nltk.FreqDist(all_words)
freq_dist.most_common(20)