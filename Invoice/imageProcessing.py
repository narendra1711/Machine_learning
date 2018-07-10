# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 22:03:38 2018

@author: narendra
"""
#------------------------------------------------------------------------------------------
#Import Libraries
import pandas as pd
import numpy as np
#------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------
#Declaring all the variables
inputFileName="input_boundaries.txt"
horiFileName="Horizontal_Keys.txt"
vertiFileName="Vertical_Keys.txt"
tabularFileName="Tabular_Keys.txt"
imagePath="pic.jpg"
#------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------
#Reading the input file(Output of Vision API)
def readInputFile(filename):
    word_infos=[]
    dict={}
    f = open(filename,'r')
    
    for line in f:
        dict={"boundingBox":line.strip().split('\'')[3],
            "text":line.strip().split('\'')[7]}
        word_infos.append(dict)
    return word_infos
#------------------------------------------------------------------------------------------
word_infos=readInputFile(inputFileName)
#------------------------------------------------------------------------------------------
#Function to create word_infos DataFrame
def create_word_infosDataframe(word_infos):
    df=pd.DataFrame(word_infos)
    df = df.join(pd.DataFrame(df['boundingBox'].str.split(',').tolist(),columns = ['x1','y1','x2','y2']))
    del df['boundingBox']
    df.x1 = df.x1.astype(np.int64)
    df.y1 = df.y1.astype(np.int64)
    df.x2 = df.x2.astype(np.int64)
    df.y2 = df.y2.astype(np.int64)
    return df

#------------------------------------------------------------------------------------------
df=create_word_infosDataframe(word_infos)
#------------------------------------------------------------------------------------------
#List of key words should be in List of Lists format(This varies from invoice-invoice)
def readKeywords():
    horiFile = open(horiFileName,'r')
    vertiFile = open(vertiFileName,'r')
    tabFile = open(tabularFileName,'r')
    keys=[]

    for line in horiFile:
        string=line.split(),"Horizontal"
        keys.append(string)

    for line in vertiFile:
        string=line.split(),"Vertical"
        keys.append(string)
        
    for line in tabFile:
        string=line.split(),"Tabular"
        keys.append(string)        
    
    return keys
#------------------------------------------------------------------------------------------
keys=readKeywords()
#------------------------------------------------------------------------------------------
