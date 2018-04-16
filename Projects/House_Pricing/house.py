# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 08:14:30 2018

@author: narendra
"""

#Loading libraries 
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (10.0, 8.0)
import seaborn as sns
from scipy import stats
from scipy.stats import norm

#loading data
train = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")

train.head()

print ('The train data has {0} rows and {1} columns'.format(train.shape[0],train.shape[1]))
print ('----------------------------')
print ('The test data has {0} rows and {1} columns'.format(test.shape[0],test.shape[1]))

train.info()

train.columns[train.isnull().any()]

'''Out of 81 features, 19 features have missing values. 
Let's check the percentage of missing values in these columns.'''
#missing value counts in each of these columns
miss = train.isnull().sum()/len(train)
miss = miss[miss > 0]
miss.sort_values(inplace=True)
miss

'''We can infer that the variable PoolQC has 99.5% missing values followed by MiscFeature, 
Alley, and Fence. Let's look at a pretty picture explaining these 
missing values using a bar plot.'''

#visualising missing values
miss = miss.to_frame()
miss.columns = ['count']
miss.index.names = ['Name']
miss['Name'] = miss.index

#plot the missing value count
sns.set(style="whitegrid", color_codes=True)
sns.barplot(x = 'Name', y = 'count', data=miss)
plt.xticks(rotation = 90)
sns.plt.show()

'''Let's proceed and check the distribution of the target variable.'''
#SalePrice
sns.distplot(train['SalePrice'])

'''We see that the target variable SalePrice has a right-skewed distribution. 
We'll need to log transform this variable so that it becomes normally distributed. 
A normally distributed (or close to normal) target variable helps in better modeling the 
relationship between target and independent variables. In addition, 
linear algorithms assume constant variance in the error term. Alternatively, 
we can also confirm this skewed behavior using the skewness metric.'''
#skewness
print("The skewness of SalePrice is {}".format(train['SalePrice'].skew()))

'''Let's log transform this variable and see if this variable distribution can get any closer to normal.'''
#now transforming the target variable
target = np.log(train['SalePrice'])
print ('Skewness is', target.skew())
sns.distplot(target)


#separate variables into new data frames
numeric_data = train.select_dtypes(include=[np.number])
cat_data = train.select_dtypes(exclude=[np.number])
print("There are {} numeric and {} categorical columns in train data".format(numeric_data.shape[1],cat_data.shape[1]))
del numeric_data['Id']

#correlation plot
corr = numeric_data.corr()
sns.heatmap(corr)

print (corr['SalePrice'].sort_values(ascending=False)[:15], '\n') #top 15 values
print ('----------------------')
print (corr['SalePrice'].sort_values(ascending=False)[-5:]) #last 5 values`


train['OverallQual'].unique()

#let's check the mean price per quality and plot it.
pivot = train.pivot_table(index='OverallQual', values='SalePrice', aggfunc=np.median)
pivot.sort