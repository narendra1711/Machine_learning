#Import Libraries
import pandas as pd
import numpy as np
import cv2
#------------------------------------------------------------------------------------------
inputFileName=r"D:\Study\Code\OCR_Invoice\Steps\Invoice_A_Boundaries.txt"
fileName = "Keys.csv"
#------------------------------------------------------------------------------------------
#This function is used to read the input file and return the dataframe(df)
def readInputFile(inputFileName):
    with open(inputFileName, 'r') as f:
        content = f.readlines()
    df = pd.DataFrame([(keys.strip().split('\'')[7]+"~"+keys.strip().split('\'')[3]).split('~') for keys in content],columns=['text','boundaries'])
    df = df.join(df.boundaries.str.split(',',expand=True)).rename(columns={0: "x1", 1: "y1", 2: "x2", 3: "y2"})
    del df['boundaries']
    df.x1 = df.x1.astype(np.int64)
    df.y1 = df.y1.astype(np.int64)
    df.x2 = df.x2.astype(np.int64)
    df.y2 = df.y2.astype(np.int64)
    return df
#------------------------------------------------------------------------------------------
df=readInputFile(inputFileName)
#------------------------------------------------------------------------------------------
#This function read the keys.csv file and returns 2lists(keys,master_keys)
def readKeywords(fileName):
    df_InputKeys = pd.read_csv(fileName)
    key = list(df_InputKeys.Keys[df_InputKeys.Keys.notnull()])
    masterKeys = list(df_InputKeys.Master_Keys[df_InputKeys.Master_Keys.notnull()])
    sub_keys = []
    for line in key:
        string = (line.split())
        sub_keys.append(string)
    master_keys=[]
    for line in masterKeys:
        master_keys.append(line.strip()) 
    return sub_keys,master_keys
#------------------------------------------------------------------------------------------
keys,master_keys = readKeywords(fileName)
#------------------------------------------------------------------------------------------
#This function generates boundaries of gives keywords the same keys format
def genKeyBoundaries(df,keys):
    for i in range(0,len(keys)):
        for j in range(0,len(keys[i])):
            for k in range(0,len(df)): 
                if(keys[i][j] == df.text[k]):
                    if(len(keys[i])!=1):
                        if (j!=0):
                            if( keys[i][j-1]['text'] == df.text[k-1]):    
                                keys[i][j]={"text":df.text[k],"value":[df.x1[k],df.y1[k],df.x2[k],df.y2[k]]}
                            else:
                                continue
                        elif(j==0):
                            if(keys[i][j+1]==df.text[k+1]):
                                keys[i][j]={"text":df.text[k],"value":[df.x1[k],df.y1[k],df.x2[k],df.y2[k]]}
                            else:
                                continue    
                        keys[i][j]={"text":df.text[k],"value":[df.x1[k],df.y1[k],df.x2[k],df.y2[k]]}
                    else:
                        keys[i][j]={"text":df.text[k],"value":[df.x1[k],df.y1[k],df.x2[k],df.y2[k]]}
    return keys
#------------------------------------------------------------------------------------------
keys=genKeyBoundaries(df,keys)
#------------------------------------------------------------------------------------------        
#Creating Keys Dataframe
def create_keysDataframe(keys):
    ind_keys=[]
    for i in range(0,len(keys)):
        for j in range(0,len(keys[i])):
            ind_keys.append({'text':keys[i][j]['text'],'x1':keys[i][j]['value'][0],'y1':keys[i][j]['value'][1],'x2':keys[i][j]['value'][2],'y2':keys[i][j]['value'][3]})                
    df_keys=pd.DataFrame(ind_keys)        
    columnsTitles=['text','x1','y1','x2','y2']   
    df_keys=df_keys.reindex(columns=columnsTitles)   
    return df_keys
#------------------------------------------------------------------------------------------
df_keys=create_keysDataframe(keys)
#------------------------------------------------------------------------------------------
#Grouping key in a list and convert to a dataframe(df_final)
def groupKeyWords(keys):
    final=[]
    dummy={}
    a=''
    for i in range(0,len(keys)):
        a=''
        x1=keys[i][0]['value'][0]
        y1=keys[i][0]['value'][1]
        x2=keys[i][0]['value'][2]
        y2=keys[i][0]['value'][3]
        for j in range(0,len(keys[i])):
            x2_temp=keys[i][len(keys[i])-1]['value'][2]
            a=' '.join([a,keys[i][j]['text']])
            x1=min(x1,keys[i][j]['value'][0])
            y1=min(y1,keys[i][j]['value'][1])
            x2=max(x1,keys[i][j]['value'][0])+x2_temp-min(x1,keys[i][j]['value'][0])
            y2=max(y2,keys[i][j]['value'][3])
        dummy={"text":a,"x1":x1,"y1":y1,"x2":x2,"y2":y2}
        final.append(dummy)
    return pd.DataFrame(final)
#------------------------------------------------------------------------------------------
df_final=groupKeyWords(keys)
columnsTitles=['text','x1','y1','x2','y2']   
df_final=df_final.reindex(columns=columnsTitles) 
#------------------------------------------------------------------------------------------
#This function appends df and df_keys, resets index and convert to a df_total dataframe
def append_resetIndex(df, df_keys):
    frames=[df, df_keys.iloc[:,0:5]]
    s1 = pd.concat(frames)
    df_subtotal=s1.drop_duplicates(keep=False)
    total=[df_subtotal,df_final]
    df_total=pd.concat(total)
    df_total=df_total.reset_index(drop=True)
    df_subtotal=df_subtotal.reset_index(drop=True)
    return df_total,df_subtotal
#------------------------------------------------------------------------------------------
df_total,df_subtotal=append_resetIndex(df, df_keys)
#------------------------------------------------------------------------------------------
columnsTitles=['text','x1','y1','x2','y2']   
df_total=df_total.reindex(columns=columnsTitles)
image_path=r"D:\Study\Code\OCR_Invoice\Steps\Order-0.png"
#------------------------------------------------------------------------------------------
#This function is mainly used to draw a Rectangle by accepting (x1,y1) and (x2,y2)
image=cv2.imread(image_path)
def drawRectangle(text,x1,y1,x2,y2):
    cv2.rectangle(image,(x1,y1) , (x1+x2,y1+y2), (0,0,255),1)
    return
for i in range(0,len(df_final)):
    drawRectangle(df_final['text'][i],df_final['x1'][i],df_final['y1'][i],df_final['x2'][i],df_final['y2'][i])

cv2.imwrite('D:\Study\Code\OCR_Invoice\Steps\Rectangled.png', image)
#------------------------------------------------------------------------------------------
#This function return the nearest right key word (df)
def nearestRightKey(Key):
    df_NoKeyword = df_final[~df_final['text'].str.contains(searchString)]
    df_NoKeyword=df_NoKeyword.reset_index(drop=True)
    df_Keyword = df_final[df_final['text'].str.contains(searchString)]
    df_Keyword=df_Keyword.reset_index(drop=True)
    df_sameY1=df_NoKeyword.loc[df_NoKeyword['y1'] == df_Keyword['y1'].iloc[0]]
    df_RightKey=df_NoKeyword[df_NoKeyword['x1'] == df_sameY1.x1.min()]
    return df_RightKey

searchString="Name:"
df_RightKey = nearestRightKey(searchString)
df_RightKey = df_RightKey.reset_index(drop=True)
df_KeyWord = df_final[df_final['text'].str.contains(searchString)]
df_KeyWord = df_KeyWord.reset_index(drop=True)
#------------------------------------------------------------------------------------------
#This function extracts data between Key and NearestRightKey
def extractDataKeyRightKey(key,RightKey):
    df_data = df_total[(df_KeyWord.x1.iloc[0] < df_total.x1)&
             (df_RightKey.x1.iloc[0] > df_total.x1)&
             (df_KeyWord.y1.iloc[0] == df_total.y1)]
    return df_data

df_data = extractDataKeyRightKey(df_KeyWord,df_RightKey)
df_data = df_data.reset_index(drop=True)
#------------------------------------------------------------------------------------------
#This function return the nearest bottom key word (df)

#------------------------------------------------------------------------------------------


