# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 18:53:30 2018
http://pythonforengineers.com/introduction-to-nltk-natural-language-processing-with-python/
@author: narendra
"""

import nltk
#nltk.download()
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk import pos_tag
sentence = "The Quick brown fox, Jumps over the lazy little dog. Hello World."
sentence.split(" ")

'''We can split the function on a space (” “) to get all the words. 
The problem with this is, we cannot extract punctuation marks like full stops, 
and this simple parser will not be able to handle every single type of sentence.'''
word_tokenize(sentence)

'''Another useful feature is that nltk can figure out if a parts of a sentence are nouns, adverbs, verbs etc.

The pos_tag() works on the output of word_tokenize():'''
w = word_tokenize(sentence)
nltk.pos_tag(w)

#If you want to know what those tags mean, you can search for them online, or use the inbuilt functions:
nltk.help.upenn_tagset()

syn = wordnet.synsets("computer")
print(syn)
print(syn[0].name())
print(syn[0].definition())
 
print(syn[1].name())
print(syn[1].definition())

syn = wordnet.synsets("talk")
syn[0].examples()

#Hypernym is the root of the word, color in the image above. Hyponyms are similar words, like the colors red blue green etc.
syn = wordnet.synsets("speak")[0]
 
print(syn.hypernyms())
 
print(syn.hyponyms())

syn = wordnet.synsets("good")
for s in syn:
    for l in s.lemmas():
        if (l.antonyms()):
            print(l.antonyms())
            
syn = wordnet.synsets("book")
for s in syn:
    print(s.lemmas())