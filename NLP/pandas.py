# -*- coding: utf-8 -*-
"""
Created on Mon May 21 16:13:07 2018

@author: Narendra_Mugada
"""

subscription_key = "d91ca35819a44f06aa2d69b214b2f6a1"
assert subscription_key
vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/"
vision_analyze_url = vision_base_url + "analyze"
#image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Atomist_quote_from_Democritus.png/338px-Atomist_quote_from_Democritus.png"

import requests

image_path=r"D:\Project\pic.jpg"
image_data = open(image_path, "rb").read()

ocr_url = vision_base_url + "ocr"
print(ocr_url)

headers  = {'Ocp-Apim-Subscription-Key': subscription_key,"Content-Type": "application/octet-stream" }
params   = {'language': 'unk', 'detectOrientation ': 'true','visualFeatures': 'Categories,Description,Color'}
#data     = {'url': image_url}
response = requests.post(ocr_url, headers=headers, params=params, data=image_data, verify=False)
response.raise_for_status()

analysis = response.json()

line_infos = [region["lines"] for region in analysis["regions"]]
word_infos = []
for line in line_infos:
    for word_metadata in line:
        for word_info in word_metadata["words"]:
            word_infos.append(word_info)
word_infos

import requests
import cv2
import pandas as pd
import numpy as np
#Reading an image
image=cv2.imread("pic.jpg")

#Input values in a dict
text_loc=word_infos
'''text_loc.append({"text":"Ordering","boundingBox":"45,157,85,167"})
text_loc.append({"text":"address","boundingBox":"89,157,126,167"})
text_loc.append({"text":"Metsa","boundingBox":"45,175,80,185"})
text_loc.append({"text":"Wood","boundingBox":"84,175,118,185"})
text_loc.append({"text":"Kerto","boundingBox":"123,175,154,185"})
text_loc.append({"text":"Punkaharaju","boundingBox":"159,175,225,185"})
text_loc.append({"text":"Box","boundingBox":"75,191,97,201"})
text_loc.append({"text":"4607","boundingBox":"101,191,130,201"})
text_loc.append({"text":"02020","boundingBox":"45,206,80,216"})
text_loc.append({"text":"Metsal","boundingBox":"85,206,131,216"})'''

def createDateframe(text_loc) :
    df=pd.DataFrame(text_loc)
    df = df.join(pd.DataFrame(df['boundingBox'].str.split(',').tolist(),columns = ['x1','y1','x2','y2']))
    del df['boundingBox']
    df.x1 = df.x1.astype(np.int64)
    df.y1 = df.y1.astype(np.int64)
    df.x2 = df.x2.astype(np.int64)
    df.y2 = df.y2.astype(np.int64)
    return df

df=createDateframe(text_loc)

#Function to draw a rectangle
def drawRectangle(text,x1,y1,x2,y2):
    cv2.rectangle(image,(x1,y1) , (x1+x2,y1+y2), (0,0,255),1)
    return

for i in range(0,len(text_loc)):
    drawRectangle(df['text'][i],df['x1'][i],df['y1'][i],df['x2'][i],df['y2'][i])

cv2.imshow('Detected',image)
cv2.waitKey(0)
cv2.destroyAllWindows()

'''def ishorizontal(box1,box2):
    if((box1['x1'][i] != box2['x1'][i+1]) and (box1['y1'][i] == box2['y1'][i+1])) :
        print(box1['text'][i],box2['text'][i+1])
    return
print ("\nhorizontal words:\n")
for i in range(0,len(text_loc)-1):
    ishorizontal(df[i:i+1],df[i+1:i+2])
    

def isvertical(box1,box2):
    if((box1['y1'][i] != box2['y1'][j]) and (box1['x1'][i] == box2['x1'][j]) and i<j) :
        print(box1['text'][i],box2['text'][j])
    return
print ("\n\nvertical words:\n")
for i in range(0,len(text_loc)-1):
    for j in range(0,len(text_loc)-1):
        isvertical(df[i:i+1],df[j:j+1])'''
        
def findrow(string,df):
    if(string['y1'][7]==df['y1'][i]):
        print(df['text'][i])
    #print(string['location'][i][0])
print ("\n\nsame row words:\n")        
for i in range(0,len(text_loc)-1):    
    findrow(df[7:8],df[i:i+1])
    
def findcolumn(string,df):
    if(string['x1'][0]==df['x1'][i]):
        print(df['text'][i])
    #print(string['location'][i][0])
print ("\n\nsame column words:\n")                
for i in range(0,len(text_loc)-1):    
    findcolumn(df[0:1],df[i:i+1])
   
