#Import Libraries
import pandas as pd
import numpy as np
import cv2
 
#------------------------------------------------------------------------------------------
#Input=Output of Vision API
inputFileName="input_boundaries.txt"
#keysFileName="keys.txt"
horiFileName="Horizontal_Keys.txt"
vertiFileName="Vertical_Keys.txt"
tabularFileName="Tabular_Keys.txt"
imagePath="pic.jpg"
string="Payment Terms"

#------------------------------------------------------------------------------------------
#Function to read an input file and create word infos(Output of Vision API)
def readInputFile(inputFileName):
    word_infos=[]
    dict={}
    f = open(inputFileName,'r')
    
    for line in f:
        dict={"boundingBox":line.strip().split('\'')[3],
            "text":line.strip().split('\'')[7]}
        word_infos.append(dict)
    return word_infos

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
def readKeywords(horiFileName,vertiFileName,tabularFileName):
    horiFile = open(horiFileName,'r')
    vertiFile = open(vertiFileName,'r')
    tabFile = open(tabularFileName,'r')
    #tabularFile = open(tabularFileName,'r')
    sub_keys=[]
    #tab_keys=[]

    for line in horiFile:
        string=line.split(),"Horizontal"
        sub_keys.append(string)

    for line in vertiFile:
        string=line.split(),"Vertical"
        sub_keys.append(string)
        
    for line in tabFile:
        string=line.split(),"Tabular"
        sub_keys.append(string)        
    
    return sub_keys
keys=[]
keys=readKeywords(horiFileName,vertiFileName,tabularFileName)

#keys=[["Please","deliver","to:"],['Purchase','Order'],['Ordering','address'],['Date'],['Vendor','address'],['Your','Vendor','No.','with','us:'],['Delivery','Date:'],['Contact','Person'],['PO','Number'],['Our','VAT','Registration','No.'],['Terms','of','Payment'],['Item'],['Material'],['Description'],['Order','quantity'],['Total','net','item','value'],['Telephone'],['Fax'],['Currency'],['Total','weight'],['Total','volume'],['Head','Office'],['Invoice','Address'],['Ordering','Office'],['Unit'],['Net','price'],['Net','value'],['Unit']]
#keys=[['Item'],['Material'],['Description'],['Order','quantity'],['Total','net','item','value']]
#keys=[["Please","deliver","to:"],['Purchase','Order'],['Ordering','address'],['Date'],['Vendor','address'],['Your','Vendor','No.','with','us:'],['Delivery','Date:'],['Contact','Person'],['PO','Number'],['Our','VAT','Registration','No.'],['Terms','of','Payment'],['Telephone'],['Fax'],['Currency']]
#------------------------------------------------------------------------------------------
keys_bound=keys.copy()

df_temp_keys=pd.DataFrame(keys_bound,columns=["text","position"])
#------------------------------------------------------------------------------------------
#This function generates boundaries of gives keywords the same keys format
def genKeyBoundaries(df,keys):
    for i in range(0,len(keys)):
        for j in range(0,len(keys[i][0])):
            for k in range(0,len(df)): 
                if (keys[i][0][j] == df.text[k] ):
                    if(len(keys[i][0])!=1):
                        if (j!=0):
                            if( keys[i][0][j-1]['text'] == df.text[k-1]):    
                                keys_bound[i][0][j]={"text":df.text[k],"value":[df.x1[k],df.y1[k],df.x2[k],df.y2[k]]}
                            else:
                                continue
                        elif(j==0):
                            if(keys[i][0][j+1]==df.text[k+1]):
                                keys_bound[i][0][j]={"text":df.text[k],"value":[df.x1[k],df.y1[k],df.x2[k],df.y2[k]]}
                            else:
                                continue    
                        keys_bound[i][0][j]={"text":df.text[k],"value":[df.x1[k],df.y1[k],df.x2[k],df.y2[k]]}
                    else:
                        keys_bound[i][0][j]={"text":df.text[k],"value":[df.x1[k],df.y1[k],df.x2[k],df.y2[k]]}
    return keys_bound

keys_bound=genKeyBoundaries(df,keys)

#------------------------------------------------------------------------------------------
#Creating Keys Dataframe
def create_keysDataframe(keys_bound):
    ind_keys=[]
    for i in range(0,len(keys_bound)):
        for j in range(0,len(keys_bound[i][0])):
            ind_keys.append({'text':keys_bound[i][0][j]['text'],'x1':keys_bound[i][0][j]['value'][0],'y1':keys_bound[i][0][j]['value'][1],'x2':keys_bound[i][0][j]['value'][2],'y2':keys_bound[i][0][j]['value'][3],'pos':keys_bound[i][1]})                
    df_keys=pd.DataFrame(ind_keys)        
    columnsTitles=['text','x1','y1','x2','y2','pos']   
    df_keys=df_keys.reindex(columns=columnsTitles)   
    return df_keys

df_keys=create_keysDataframe(keys_bound)

#------------------------------------------------------------------------------------------
#Grouping key in a list
def groupKeyWords(keys_bound):
    final=[]
    dummy={}
    a=''
    for i in range(0,len(keys_bound)):
        a=''
        x1=keys_bound[i][0][0]['value'][0]
        y1=keys_bound[i][0][0]['value'][1]
        x2=keys_bound[i][0][0]['value'][2]
        y2=keys_bound[i][0][0]['value'][3]
        for j in range(0,len(keys_bound[i][0])):
            x2_temp=keys_bound[i][0][len(keys_bound[i][0])-1]['value'][2]
            a=' '.join([a,keys_bound[i][0][j]['text']])
            x1=min(x1,keys_bound[i][0][j]['value'][0])
            y1=min(y1,keys_bound[i][0][j]['value'][1])
            x2=max(x1,keys_bound[i][0][j]['value'][0])+x2_temp-min(x1,keys_bound[i][0][j]['value'][0])
            y2=max(y2,keys_bound[i][0][j]['value'][3])
            pos=keys_bound[i][1]
        dummy={"text":a,"x1":x1,"y1":y1,"x2":x2,"y2":y2,"pos":pos}
        final.append(dummy)
    return final

final=groupKeyWords(keys_bound)

#------------------------------------------------------------------------------------------
#Convert final grouped list to a dataframe
def createGroupedDataframe(final):
    df_final=pd.DataFrame(final)
    columnsTitles1=['text','x1','y1','x2','y2','pos']   
    df_final=df_final.reindex(columns=columnsTitles1) 
    return df_final

df_final=createGroupedDataframe(final)

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

df_total,df_subtotal=append_resetIndex(df, df_keys)

df_finalHor=df_final.loc[df_final['pos']=='Horizontal']

def Horizontal(start,end):
    subString=""
    a=[]
    
    if(end!=9999):
        print("IF")
        for i in range(0,len(df_total)):
            
            if(abs(df_finalHor.y1[start]-df_total.y1[i])<=3 and 
                   df_finalHor.x1[start]<df_total.x1[i] and
                   abs(df_finalHor.y1[start]-df_total.y1[end])>3):
                print(df_finalHor.text[start],"and",df_finalHor.text[end],"are not in same row")
                subString=subString+" "+df_total.text[i]
                a.append({"x1":df_total.x1[i],"y1":df_total.y1[i],
                          "x2":df_total.x2[i],"y2":df_total.y2[i]})
                
        
            elif(abs(df_finalHor.y1[start]-df_total.y1[i])<=3 and
                     df_finalHor.x1[start]<df_total.x1[i] and
                     df_finalHor.x1[end]>df_total.x1[start] and
                     abs(df_finalHor.y1[start]-df_total.y1[end])<=3):
                print(df_finalHor.text[start],df_finalHor.text[end],"are in same row")
                subString=subString+" "+df_total.text[i]
                a.append({"x1":df_total.x1[i],"y1":df_total.y1[i],
                          "x2":df_total.x2[i],"y2":df_total.y2[i]})
                #print(df_total.text[i])
    elif(end==9999):
        print("ELSE")
        for i in range(0,len(df_total)):
            if(abs(df_finalHor.y1[start]-df_total.y1[i])<=3 and 
                   df_finalHor.x1[start]<df_total.x1[i]):
                print(df_finalHor.text[start],"is the last index in df_finalHor")
                print(df_total.text[i])
                subString=subString+" "+df_total.text[i]
                a.append({"x1":df_total.x1[i],"y1":df_total.y1[i],
                          "x2":df_total.x2[i],"y2":df_total.y2[i]})
                #print(df_total.text[i])
    a=pd.DataFrame(a)
    print(a)
    x1=a.x1.min()
    y1=a.y1.min()
    x2=(a.x1+a.x2).max()-a.x1.min()
    y2=a.y2.max()
    return subString,x1,y1,x2,y2


for i in range(0,len(df_finalHor)):
    if(string.strip()==df_finalHor.text[i].strip() and i!=len(df_finalHor)-1):
        start=i
        end=start+1
    elif(string.strip()==df_finalHor.text[i].strip() and i==len(df_finalHor)-1):
        start=i
        end=9999
#print(start,end)
subString,x1,y1,x2,y2=Horizontal(start,end)   

#print(subString,x1,y1,x2,y2)     

image_path=imagePath
image=cv2.imread(image_path)
def drawRectangleKey(text,x1,y1,x2,y2):
    cv2.rectangle(image,(x1,y1) , (x1+x2,y1+y2), (0,0,255),1)
    return

drawRectangleKey("text",df_finalHor.x1[start],df_finalHor.y1[start],
                 df_finalHor.x2[start],df_finalHor.y2[start])

def drawRectangleValue(text,x1,y1,x2,y2):
    cv2.rectangle(image,(x1,y1) , (x1+x2,y1+y2), (0,100,0),1)
    return

drawRectangleValue("text",x1,y1,x2,y2)

cv2.imshow('Detected',image)
cv2.waitKey(0)
cv2.destroyAllWindows()