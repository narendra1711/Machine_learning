# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 07:19:23 2018

@author: narendra
"""
#Importing Packages
import pandas as pd
import matplotlib as plt
import numpy as np

#Read Dataset
dataset=pd.read_csv("reviews.csv",header=None)

#Rename Column names in a dataset
dataset=dataset.rename(columns={0:'Review',1:'Rating'})

review=dataset.iloc[:,0]

import nltk
from nltk.corpus import stopwords
import re

corpus=[]
for item in range(0,10):
    #Reviews should contain only alphabets
    reviews=re.sub('[^a-zA-Z]',' ',review[item])
    
    #Convert reviews to lower-case
    reviews=reviews.lower()
    
    #Stop unnecessary words in the reviews

    
    #Download stopwords packages
    nltk.download('stopwords')
    
    #Split the review into words 
    #Stem the word
    from nltk.stem.porter import PorterStemmer
    ps=PorterStemmer()
    reviews=reviews.split()
    reviews=[ps.stem(word) for word in reviews if not word in set(stopwords.words('english'))]
    reviews=" ".join(reviews)
    corpus.append(reviews)

from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer(max_features=15)
X=cv.fit_transform(corpus).toarray()
y=dataset.iloc[:,1]

# Splitting the dataset into the Training set and Test set
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.5, random_state = 0)

# Fitting Naive Bayes to the Training set
from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)