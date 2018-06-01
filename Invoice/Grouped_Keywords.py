# -*- coding: utf-8 -*-
"""
Created on Thu May 24 10:07:17 2018

@author: Narendra_Mugada
"""

import pandas as pd
import numpy as np
import cv2
import pdb

word_infos=[]
dict={}
f = open('input_boundaries.txt','r')

for line in f:
    dict={"boundingBox":line.strip().split('\'')[3],
            "text":line.strip().split('\'')[7]}
    word_infos.append(dict)
image_path=r"D:\project\input.png"
image=cv2.imread(image_path)
def drawRectangle(text,x1,y1,x2,y2):
    cv2.rectangle(image,(x1,y1) , (x1+x2,y1+y2), (0,0,255),1)
    return 
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Dataframe for words_info
df=pd.DataFrame(word_infos)
df = df.join(pd.DataFrame(df['boundingBox'].str.split(',').tolist(),columns = ['x1','y1','x2','y2']))
del df['boundingBox']
df.x1 = df.x1.astype(np.int64)
df.y1 = df.y1.astype(np.int64)
df.x2 = df.x2.astype(np.int64)
df.y2 = df.y2.astype(np.int64)

'''for i in range(0,len(df)):
    drawRectangle(df['text'][i],df['x1'][i],df['y1'][i],df['x2'][i],df['y2'][i])
    
cv2.imshow('Detected',image)
cv2.waitKey(0)
cv2.destroyAllWindows()'''

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#giving boudaries for keywords
keys=[["Please","deliver","to:"],['Purchase','Order'],['Ordering','address'],['Date'],['Vendor','address'],['Your','Vendor','No.','with','us:'],['Delivery','Date:'],['Contact','Person'],['PO','Number'],['Our','VAT','Registration','No.']]
#keys=[['Your','Vendor','No.','with','us:']]
keys_bound=keys.copy()

for i in range(0,len(keys)):
    for j in range(0,len(keys[i])):
        for k in range(0,len(df)): 
            if (keys[i][j] == df.text[k] ):
                if(len(keys[i])!=1):
                    if (j==len(keys[i])-1 or j!=0):
                        if( keys[i][j-1]['text'] == df.text[k-1]):
                            keys_bound[i][j]={"text":df.text[k],"value":[df.x1[k],df.y1[k],df.x2[k],df.y2[k]]}
                        else:
                            continue    
                    keys_bound[i][j]={"text":df.text[k],"value":[df.x1[k],df.y1[k],df.x2[k],df.y2[k]]}
                else:
                    keys_bound[i][j]={"text":df.text[k],"value":[df.x1[k],df.y1[k],df.x2[k],df.y2[k]]}
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#creating dataframe for keys
ind_keys=[]
for i in range(0,len(keys_bound)):
    for j in range(0,len(keys_bound[i])):
        ind_keys.append({'text':keys_bound[i][j]['text'],'x1':keys_bound[i][j]['value'][0],'y1':keys_bound[i][j]['value'][1],'x2':keys_bound[i][j]['value'][2],'y2':keys_bound[i][j]['value'][3]})                
df_keys=pd.DataFrame(ind_keys)        
columnsTitles=['text','x1','y1','x2','y2']   
df_keys=df_keys.reindex(columns=columnsTitles)    
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
'''for i in range(0,len(keys_bound)):
    for j in range(0,len(keys_bound[i])):
        drawRectangle(keys_bound[i][j]['text'],keys_bound[i][j]['value'][0],keys_bound[i][j]['value'][1],keys_bound[i][j]['value'][2],keys_bound[i][j]['value'][3])
    
cv2.imshow('Detected',image)
cv2.waitKey(0)
cv2.destroyAllWindows()'''
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#grouping keywords in a list
final=[]
dummy={}
a=''
for i in range(0,len(keys_bound)):
    a=''
    x1=keys_bound[i][0]['value'][0]
    y1=keys_bound[i][0]['value'][1]
    x2=keys_bound[i][0]['value'][2]
    y2=keys_bound[i][0]['value'][3]
    for j in range(0,len(keys_bound[i])):
        x2_temp=keys_bound[i][len(keys_bound[i])-1]['value'][2]
        a=' '.join([a,keys_bound[i][j]['text']])
        x1=min(x1,keys_bound[i][j]['value'][0])
        y1=min(y1,keys_bound[i][j]['value'][1])
        x2=max(x1,keys_bound[i][j]['value'][0])+x2_temp-min(x1,keys_bound[i][j]['value'][0])
        y2=max(y2,keys_bound[i][j]['value'][3])
        
    dummy={"text":a,"x1":x1,"y1":y1,"x2":x2,"y2":y2}
    final.append(dummy)
    
'''for i in range(0,len(final)):
    drawRectangle(final[i]['text'],final[i]['x1'],final[i]['y1'],final[i]['x2'],final[i]['y2'])
cv2.imshow('Detected',image)
cv2.waitKey(0)
cv2.destroyAllWindows()    '''
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Convert final to a dataframe
df_final=pd.DataFrame(final)
columnsTitles1=['text','x1','y1','x2','y2']   
df_final=df_final.reindex(columns=columnsTitles1)  
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Convert final to a dataframe
frames=[df, df_keys]
s1 = pd.concat(frames)
df_subtotal=s1.drop_duplicates(keep=False)
total=[df_subtotal,df_final]
df_total=pd.concat(total)
df_total=df_total.reset_index(drop=True)
image_path=r"D:\project\input.png"
image=cv2.imread(image_path)
for i in range(0,len(df_total)):
    drawRectangle(df_total['text'][i],df_total['x1'][i],df_total['y1'][i],df_total['x2'][i],df_total['y2'][i])
cv2.imshow('Detected',image)
cv2.waitKey(0)
cv2.destroyAllWindows()
