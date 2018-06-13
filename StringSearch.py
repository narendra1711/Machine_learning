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
imagePath="input.png"
string="Invoice Address"

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

#------------------------------------------------------------------------------------------
#This function extracts vertical data between two keywords
def extractVerticalData(prev,nxt):
    extract=[]
    extractedData=[]
    a=b=0
    for i in range(0,len(df)):
        txt=""
       
        if(df['x1'][i]==prev['x1'] and df['y1'][i]==prev['y1'] ):
            a=len(prev.text.split(' '))-2
            a=a+i
            #print("a",a)
            #extract.append({'text':txt+df_total['text'][i],"Boundaries":[df_total['x1'][i],df_total['y1'][i],df_total['x2'][i],df_total['y2'][i]]})
        if(df['x1'][i]==nxt['x1'] and df['y1'][i]==nxt['y1'] ):
            b=i
            #print("b",b)
    for i in range(a+1,b) :  
            extract.append({'text':txt+df['text'][i],"Boundaries":[df['x1'][i],df['y1'][i],df['x2'][i],df['y2'][i]]})
    extractedData.append({"text":prev['text'],"data":extract})
    x1=extractedData[0]['data'][0]['Boundaries'][0]
    y1=extractedData[0]['data'][0]['Boundaries'][1]
    x2=y2=x3=y3=0
    x2_temp=extractedData[0]['data'][0]['Boundaries'][2]
    y2_temp=extractedData[0]['data'][0]['Boundaries'][3]
    for j in range(0,len(extractedData[0]['data'])):
        x1=min(x1,extractedData[0]['data'][j]['Boundaries'][0])
        y1=min(y1,extractedData[0]['data'][j]['Boundaries'][1])
        if(x3<extractedData[0]['data'][j]['Boundaries'][0]):
            x2_temp=extractedData[0]['data'][j]['Boundaries'][2]
        x3=max(x3,extractedData[0]['data'][j]['Boundaries'][0])
        x2=x3+x2_temp
        #print(x2_temp)
        if(y3<extractedData[0]['data'][j]['Boundaries'][1]):
            y2_temp=extractedData[0]['data'][j]['Boundaries'][3]
        y3=max(y3,extractedData[0]['data'][j]['Boundaries'][1])
        y2=y3+y2_temp
    x2=x2-x1
    y2=y2-y1
    return (extractedData,x1,y1,x2,y2)

#------------------------------------------------------------------------------------------
#This function extracts horizaontal data between two keywords
extract=[]
extractedData=[]

def extractHorizontalData(current):
    for i in range(0,len(df_total)):
        if((abs(df_total['y1'][i]-current['y1'])<=4 ) and 
           (abs(df_total['y2'][i]-current['y2'])<=4) and
           current['x1']<=df_total['x1'][i] and
           current['text']!=df_total['text'][i]):
            output=df_total.text[i]
            x1=df_total.x1[i]
            y1=df_total.y1[i]
            x2=df_total.x2[i]
            y2=df_total.y2[i]
            text=current['text']
            extractedData.append({"text":current['text'],
                                  "data":[{"text":df_total['text'][i],
                                           "Boundaries":[df_total.x1[i],
                                                         df_total.y1[i],
                                                         df_total.x2[i],
                                                         df_total.y2[i]]
                                           }]})
                                           
    return (text,x1,y1,x2,y2,output)
#------------------------------------------------------------------------------------------
#This function extratcs tabular data
dummy=[]
st="Total net item value"
def extractTabularData(prev,nxt):
    boundary=""
    for i in range(0,len(df_total)):
        if(df_total.text[i].strip()==st.strip() and st.strip() not in ("Head Office","Invoice Address","Ordering Office") ):
            boundary=df_total.iloc[i]
            print("IN")
        else:
            boundary=""
    print("Boundary",boundary)
    for i in range(0,len(df_total)):
        if(prev['x1']<=(df_total.x1[i]+2) and
           nxt['x1']-2>df_total.x1[i] and
           prev['y1']<df_total.y1[i]):
            if(boundary!=""):
                if(boundary['y1']>df_total.y1[i]):
                    dummy.append({"text":df_total.text[i],"x1":df_total.x1[i],"y1":df_total.y1[i],"x2":df_total.x2[i],"y2":df_total.y2[i]})
            else:
                
                dummy.append({"text":df_total.text[i],"x1":df_total.x1[i],"y1":df_total.y1[i],"x2":df_total.x2[i],"y2":df_total.y2[i]})
            print("IF")
    
    
        
                    
    return dummy
 
#------------------------------------------------------------------------------------------
#This function checks whether the key word should be sent to extractHorizontalData or extractVerticalData
def checkHorizontalVertical(string,horiFileName,vertiFileName,tabularFileName):
    horiFile = open(horiFileName,'r')
    vertiFile = open(vertiFileName,'r')
    tabFile = open(tabularFileName,'r')
    sub_keys=[]

    for line in horiFile:
        if (string.strip() == line.strip()):
            df_final.sort_values('pos')
            for i in range(0,len(df_finalHor)):
                if(string==df_finalHor.text[i].strip()):
                    index=i
            #print(index)
            

            text,x1,y1,x2,y2,output=extractHorizontalData(df_finalHor.iloc[index])
            print(text,output)
            
            image_path=imagePath
            image=cv2.imread(image_path)
            def drawRectangleKey(text,x1,y1,x2,y2):
                cv2.rectangle(image,(x1,y1) , (x1+x2,y1+y2), (0,0,255),1)
                return
            
            drawRectangleKey("text",df_finalHor.x1[index],df_finalHor.y1[index],df_finalHor.x2[index],df_finalHor.y2[index])
            
            def drawRectangleValue(text,x1,y1,x2,y2):
                cv2.rectangle(image,(x1,y1) , (x1+x2,y1+y2), (0,100,0),1)
                return
            
            drawRectangleValue("text",x1,y1,x2,y2)
            
            cv2.imshow('Detected',image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("hello",string,line)
    
    for line in vertiFile:
        
        if string in line:
            df_final.sort_values('pos')
            for i in range(0,len(df_finalVer)-1):
                if(string==df_finalVer.text[i].strip()):
                    index=i
                    j=index+1
            #print(df_final.sort_values('pos'))
            #print(index,j)
            
            text,x1,y1,x2,y2=extractVerticalData(df_finalVer.iloc[index],df_finalVer.iloc[j])
            #print(text,x1,y1,x2,y2)            
            #extractedData,x1,y1,x2,y2=extractVerticalData(df_final.iloc[2],df_final.iloc[3])
            #print(extractedData)
            image_path="input.png"
            image=cv2.imread(image_path)
            
            def drawRectangleKey(text,x1,y1,x2,y2):
                cv2.rectangle(image,(x1,y1) , (x1+x2,y1+y2), (0,0,255),1)
                return 
            
            drawRectangleKey('text',df_finalVer.x1[index],df_finalVer.y1[index],df_finalVer.x2[index],df_finalVer.y2[index])
            
            def drawRectangleValue(text,x1,y1,x2,y2):
                cv2.rectangle(image,(x1,y1) , (x1+x2,y1+y2), (0,100,0),1)
                return 
            drawRectangleValue('text',x1,y1,x2,y2)
            
            cv2.imshow('Detected',image)
            #cv2.imwrite(r'D:\Study\Code\OCR_Invoice\Setup\rect.png', image)
            cv2.waitKey(0)
            cv2.destroyAllWindows() 
            
    for line in tabFile:
        if string in line:
            for i in range(0,len(df_finalTab)):
                if(string==df_finalTab.text[i].strip()):
                    index=i
                    j=i+1
            #print(df_final.sort_values('pos'))
            #print(index,j)
            #text,x1,y1,x2,y2=extractTabularData(df_finalTab.iloc[index],df_finalTab.iloc[j])
            print(index,j)
            dummy=extractTabularData(df_finalTab.iloc[index],df_finalTab.iloc[j]) 
            
            image_path="input.png"
            image=cv2.imread(image_path)
            def drawRectangleKey(text,x1,y1,x2,y2):
                    cv2.rectangle(image,(x1,y1) , (x1+x2,y1+y2), (0,0,255),1)
                    return 
                
            drawRectangleKey('text',df_finalTab.x1[index],df_finalTab.y1[index],df_finalTab.x2[index],df_finalTab.y2[index])
            for i in range(0,len(dummy)):
                def drawRectangleValue(text,x1,y1,x2,y2):
                    cv2.rectangle(image,(x1,y1) , (x1+x2,y1+y2), (0,100,0),1)
                    return 
                drawRectangleValue('text',dummy[i]['x1'],dummy[i]['y1'],dummy[i]['x2'],dummy[i]['y2'])
                
                #cv2.imshow('Detected',image)
                cv2.imwrite(r'D:\Study\Code\OCR_Invoice\Setup\rect.png', image)
                #cv2.waitKey(0)
                #cv2.destroyAllWindows()
            #print(text,x1,y1,x2,y2)            
            #extractedData,x1,y1,x2,y2=extractTabularData(df_final.iloc[index],df_final.iloc[3])
            #print(extractedData)
    return sub_keys

df_final=df_final.reset_index(drop=True)
df_total=df_total.sort_values('x1')
df_total=df_total.reset_index(drop=True)
df_final=df_final.sort_values('y1')
df_final=df_final.reset_index(drop=True)
df_total=df_total.sort_values('y1')
df_total=df_total.reset_index(drop=True)
df_final=df_final.sort_values('y1')
df_total=df_total.reset_index(drop=True)
df_finalHor=df_final.loc[df_final['pos']=='Horizontal']
df_finalVer=df_final.loc[df_final['pos']=='Vertical']  
df_finalTab=df_final.loc[df_final['pos']=='Tabular'] 
df_finalHor=df_finalHor.reset_index(drop=True)
df_finalVer=df_finalVer.reset_index(drop=True)
df_finalTab=df_finalTab.reset_index(drop=True)
df_finalTab.sort_values(['y1','x2'],ascending=[False,False])



checkHorizontalVertical(string,horiFileName,vertiFileName,tabularFileName)

  

#--------------------------------------------------------------------------------------------
  

