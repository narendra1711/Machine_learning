# -*- coding: utf-8 -*-
"""
Created on Tue May 29 18:14:58 2018

@author: narendra
"""

import pandas as pd
import numpy as np
import cv2

word_infos=[]
dict={}
f = open('Input.txt','r')
for line in f:
    dict={"boundingBox":line.strip().split('\'')[3],
            "text":line.strip().split('\'')[7]}
    word_infos.append(dict)
#------------------------------------------------------------------------------
#Input Dataframe with all boundaries
input_df=pd.DataFrame(word_infos)
input_df = input_df.join(pd.DataFrame(input_df['boundingBox'].str.split(',').tolist(),columns = ['x1','y1','x2','y2']))
del input_df['boundingBox']
input_df.x1 = input_df.x1.astype(np.int64)
input_df.y1 = input_df.y1.astype(np.int64)
input_df.x2 = input_df.x2.astype(np.int64)
input_df.y2 = input_df.y2.astype(np.int64)
input_df['X'] = input_df.x1+input_df.x2
input_df['Y'] = input_df.y1+input_df.y2
#------------------------------------------------------------------------------
#Keywords Dataframe with all boundaries
keywords=["BILL","TO:","SHIPPING","Invoice","#","Date","Name","of","Rep.","Contact","Phone","Payment","Terms"]
key=[]
temp_dic={}
for i in range(0,len(input_df)):
    for j in range(0,len(keywords)):
        if(input_df.text[i]==keywords[j]):
            temp_dic={"text":input_df.text[i],
                      "x1":input_df.x1[i],
                      "y1":input_df.y1[i],
                      "x2":input_df.x2[i],
                      "y2":input_df.y2[i]}
            key.append(temp_dic)

keywords_df=pd.DataFrame(key) 
keywords_df["X"]=keywords_df.x1+keywords_df.x2
keywords_df["Y"]=keywords_df.y1+keywords_df.y2           
#------------------------------------------------------------------------------
#Grouped Keywords Dataframe with all boundaries
TOL=3
str=""
dic={}

lis=[]
for i in range(0,len(keywords_df)-1):
    #print(keywords_df.text[i])
    #print(keywords_df.text[i+1])
    if(abs(keywords_df.y1[i+1]-keywords_df.y1[i])<=TOL):
        if(str!=""):
            str=str+" "+keywords_df.text[i]
            dic={"text":str}
            lis.append(dic)
            print(str)
        else:
            str=str+keywords_df.text[i]
        if(i==len(keywords_df)-2):
            str=str+ " "+ keywords_df.text[i+1]
            print(str)
            dic={"text":str}
            lis.append(dic)
        #print(keywords_df.text[i], keywords_df.text[i+1])
    else:
        if(i!=0 and abs(keywords_df.y1[i-1]-keywords_df.y1[i])<=TOL):
            str=str+ " " +keywords_df.text[i]
            print(str)
            dic={"text":str}
            lis.append(dic)
            str=""
            
        
