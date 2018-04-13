# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 19:15:13 2018

@author: narendra
"""
#Importing Headers
import pandas as pd
import numpy as np

#Import dataset
train_dataset=pd.read_csv("train.csv")
test_dataset=pd.read_csv("test.csv")

train_dataset.head()
test_dataset.head()

X_train=train_dataset.iloc[:,[0,2,4,5,6,7,9,11]]

X_train.isnull().sum()

y_train=train_dataset.iloc[:,1]

X_test=test_dataset.iloc[:,[0,1,3,4,5,6,8,10]]

#Imputer for missing values
from sklearn.preprocessing import Imputer

imputer=Imputer(missing_values="NaN",strategy="mean",axis=0)

X_train.iloc[:,3:4]=imputer.fit_transform(X_train.iloc[:,3:4])

X_test.iloc[:,3:4]=imputer.fit_transform(X_test.iloc[:,3:4])

X_train.iloc[:,2]=X_train.iloc[:,2].replace("female",1)

X_train.iloc[:,2]=X_train.iloc[:,2].replace("male",0)

X_test.iloc[:,2]=X_test.iloc[:,2].replace("male",0)

X_test.iloc[:,2]=X_test.iloc[:,2].replace("female",1)

X_train=pd.get_dummies(X_train,columns=["Pclass","SibSp","Parch","Embarked"])

X_test.drop("Parch_9",axis=1,inplace=True)

X_test=pd.get_dummies(X_test,columns=["Pclass","SibSp","Parch","Embarked"])

X_train.isnull().sum()

X_test.iloc[:,3:4]=X_test.iloc[:,3:4].replace(np.nan,0.0)

X_test.isnull().sum()

# Fitting Logistic Regression to the Training set
from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression(random_state = 0)
classifier.fit(X_train, y_train)

#Prediction the test results
y_pred=classifier.predict(X_test)