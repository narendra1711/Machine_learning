#Import Libraries
import pandas as pd
import numpy as np
import cv2
 
#------------------------------------------------------------------------------------------
inputFileName="Quotation_Boundaries.txt"
horiFileName="Horizontal_Keys.txt"
vertiFileName="Vertical_Keys.txt"
tabularFileName="Tabular_Keys.txt"
imagePath="input.png"
#string="Contact Person"
f=open("Output.txt","w+")
#string=['Purchase Order','PO Number','Date','Our VAT Registration No.','Your Vendor No. with us:','Currency']
string=['Customer Name']
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
    sub_keys=[]

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
#Horizontal grouping
df_finalHor=df_final.loc[df_final['pos']=='Horizontal']
def Horizontal(start,end):
    subString=""
    a=[]
    
    if(end!=9999):
        print("IF")
        for i in range(0,len(df_total)):
            
            if(abs(df_finalHor.y1[start]-df_total.y1[i])<=3 and 
                   df_finalHor.x1[start]<df_total.x1[i] and
                   abs(df_finalHor.y1[start]-df_finalHor.y1[end])>3):
                print(df_finalHor.y1[start])
                print(df_finalHor.y1[end])
                print(df_finalHor.text[start],"and",df_finalHor.text[end],"are not in same row")
                subString=subString+" "+df_total.text[i]
                a.append({"x1":df_total.x1[i],"y1":df_total.y1[i],
                          "x2":df_total.x2[i],"y2":df_total.y2[i]})
                
        
            elif(abs(df_finalHor.y1[start]-df_total.y1[i])<=3 and
                     df_finalHor.x1[start]<df_total.x1[i] and
                     df_finalHor.x1[end]>df_total.x1[i] and
                     abs(df_finalHor.y1[start]-df_finalHor.y1[end])<=3):
                print(df_finalHor.text[start],df_finalHor.text[end],"are in same row")
                subString=subString+" "+df_total.text[i]
                a.append({"x1":df_total.x1[i],"y1":df_total.y1[i],
                          "x2":df_total.x2[i],"y2":df_total.y2[i]})
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
    a=pd.DataFrame(a)
    print(a)
    x1=a.x1.min()
    y1=a.y1.min()
    x2=(a.x1+a.x2).max()-a.x1.min()
    y2=a.y2.max()
    return subString,x1,y1,x2,y2
#------------------------------------------------------------------------------------------
#This function extracts vertical data between two keywords
df_finalVer=df_final.loc[df_final['pos']=='Vertical'] 
df_finalVer=df_finalVer.reset_index(drop=True)
def extractVerticalData(prev,nxt):
    extract=[]
    extractedData=[]
    a=b=0
    for i in range(0,len(df)):
        txt=""
       
        if(df['x1'][i]==prev['x1'] and df['y1'][i]==prev['y1'] ):
            a=len(prev.text.split(' '))-2
            a=a+i
        if(df['x1'][i]==nxt['x1'] and df['y1'][i]==nxt['y1'] ):
            b=i
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
        if(y3<extractedData[0]['data'][j]['Boundaries'][1]):
            y2_temp=extractedData[0]['data'][j]['Boundaries'][3]
        y3=max(y3,extractedData[0]['data'][j]['Boundaries'][1])
        y2=y3+y2_temp
    x2=x2-x1
    y2=y2-y1
    return (extractedData,x1,y1,x2,y2)

#------------------------------------------------------------------------------------------
#This function extracts tabular data
dummy=[]
df_finalTab=df_final.loc[df_final['pos']=='Tabular'] 
df_finalTab=df_finalTab.reset_index(drop=True)
def extractTabularData(start,end):
    if(end!=9999):#Data between two columns and with boundary
        prev=df_finalTab.iloc[start]
        nxt=df_finalTab.iloc[end]
        print("IF")
        if(prev.text.strip() in ('Item','Material','Description','Order quantity','Net price','Net value','Unit')):
            boundary_y1=1270
        else:
            boundary_y1=9999
        print(boundary_y1)
        for i in range(0,len(df_total)):
            if(prev['x1']<=(df_total.x1[i]+2) and
               nxt['x1']-2>df_total.x1[i] and
               prev['y1']<df_total.y1[i]):
                if(boundary_y1==1270 and df_total.y1[i]<boundary_y1  and abs(prev.y1-nxt.y1)<=5):
                    dummy.append({"text":df_total.text[i],"x1":df_total.x1[i],"y1":df_total.y1[i],"x2":df_total.x2[i],"y2":df_total.y2[i]})    
                elif(boundary_y1==9999 and abs(prev.y1-nxt.y1)>5):
                    dummy.append({"text":df_total.text[i],"x1":df_total.x1[i],"y1":df_total.y1[i],"x2":df_total.x2[i],"y2":df_total.y2[i]})
                print(dummy)
            elif(prev['x1']<=(df_total.x1[i]+2) and
               prev['y1']<df_total.y1[i] and 
               boundary_y1==1270 and 
               df_total.y1[i]<boundary_y1 and 
               abs(prev.y1-nxt.y1)>5):
                dummy.append({"text":df_total.text[i],"x1":df_total.x1[i],"y1":df_total.y1[i],"x2":df_total.x2[i],"y2":df_total.y2[i]})
        a=pd.DataFrame(dummy)
        x1=a.x1.min()
        y1=a.y1.min()
        x2=(a.x1+a.x2).max()-a.x1.min()
        y2=(a.y1+a.y2).max()-a.y1.min()
                
    elif(end==9999):#Last column value that has no boundary
        prev=df_finalTab.iloc[start]
        print(prev)
        if(prev.text.strip() in ('Item','Material','Description','Order quantity','Net price','Net value','Unit')):
            boundary_y1=1270
        else:
            boundary_y1=9999
        print(boundary_y1)
        a=[]
        for i in range(0,len(df_total)):
            if(df_total.y1[i]>prev.y1+1 and df_total.x1[i]>=prev.x1 and boundary_y1==9999):
                a.append({"text":df_total.text[i],"x1":df_total.x1[i],"y1":df_total.y1[i],
                         "x2":df_total.x2[i],"y2":df_total.y2[i]})
                print("IF")
            elif(boundary_y1==1270):
                a.append({"text":df_total.text[i],"x1":df_total.x1[i],"y1":df_total.y1[i],
                         "x2":df_total.x2[i],"y2":df_total.y2[i]})
                print("ELSE")
        a=pd.DataFrame(a)
        print(a)
        x1=a.x1.min()
        y1=a.y1.min()
        x2=(a.x1+a.x2).max()-a.x1.min()
        y2=(a.y1+a.y2).max()-a.y1.min()
    return x1,y1,x2,y2
 
#------------------------------------------------------------------------------------------
#This function checks whether the key word should be sent to extractHorizontalData or extractVerticalData
def checkHorizontalVertical(string,horiFileName,vertiFileName,tabularFileName):
    horiFile = open(horiFileName,'r')
    vertiFile = open(vertiFileName,'r')
    tabFile = open(tabularFileName,'r')
    sub_keys=[]
    
    for line in horiFile:
        for k in range(0,len(string)):
            if (str(string[k]).strip() == line.strip()):
                df_final.sort_values('pos')
            
                for i in range(0,len(df_finalHor)):
                    if(str(string[k]).strip()==df_finalHor.text[i].strip() and i!=len(df_finalHor)-1):
                        start=i
                        end=start+1
                    elif(str(string[k]).strip()==df_finalHor.text[i].strip() and i==len(df_finalHor)-1):
                        start=i
                        end=9999
                #print(start,end)
                subString,x1,y1,x2,y2=Horizontal(start,end)   
                
                #print(subString,x1,y1,x2,y2)     
                out={"Input":string[k],"Output":subString}
                f.write(out['Input']+out['Output']+"\n")
    f.close()
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
    
    #cv2.imshow('Detected',image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    cv2.imwrite(r'D:\Study\Code\OCR_Invoice\Setup\rect.png', image)
            
    for line in vertiFile:
        for k in range(0,len(string)):
            #if str(string[k]).strip in line:
            if (str(string[k]).strip() == line.strip()):
                df_final.sort_values('pos')
                for i in range(0,len(df_finalVer)-1):
                    if(str(string[k]).strip()==df_finalVer.text[i].strip()):
                        index=i
                        j=index+1
                #print(df_final.sort_values('pos'))
                #print(index,j)
                
                text,x1,y1,x2,y2=extractVerticalData(df_finalVer.iloc[index],df_finalVer.iloc[j])
                print(text)
                
                #out={"Input":string[k],"Output":text}
                #f.write(out['Input']+out['Output']+"\n")
    #f.close()
            #print(text,x1,y1,x2,y2)            
            #extractedData,x1,y1,x2,y2=extractVerticalData(df_final.iloc[2],df_final.iloc[3])
            #print(extractedData)
    image_path=imagePath
    image=cv2.imread(image_path)
    
    def drawRectangleKey(text,x1,y1,x2,y2):
        cv2.rectangle(image,(x1,y1) , (x1+x2,y1+y2), (0,0,255),1)
        return 
    
    drawRectangleKey('text',df_finalVer.x1[index],df_finalVer.y1[index],df_finalVer.x2[index],df_finalVer.y2[index])
    
    def drawRectangleValue(text,x1,y1,x2,y2):
        cv2.rectangle(image,(x1,y1) , (x1+x2,y1+y2), (0,100,0),1)
        return 
    drawRectangleValue('text',x1,y1,x2,y2)
    
    #cv2.imshow('Detected',image)
    cv2.imwrite(r'D:\Study\Code\OCR_Invoice\Setup\rect.png', image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows() 
    for line in tabFile:
        if (string.strip() == line.strip()):
            df_final.sort_values('pos')
            for i in range(0,len(df_finalTab)):
                if(string.strip()==df_finalTab.text[i].strip()):
                    if(i!=len(df_finalTab)-1):
                        start=i
                        end=i+1
                    else:
                        start=i
                        end=9999
                    x1,y1,x2,y2=extractTabularData(start,end)
            print(x1,y1,x2,y2)
            index=0
            for j in range(0,len(df_finalTab)):
                if(string.strip()==df_finalTab.text[j].strip()):
                    index=j
            print(index)
            image_path=imagePath
            image=cv2.imread(image_path)
            def drawRectangleKey(text,x1,y1,x2,y2):
                cv2.rectangle(image,(x1,y1) , (x1+x2,y1+y2), (0,0,255),1)
                return 
            drawRectangleKey('text',df_finalTab.x1[index],df_finalTab.y1[index],df_finalTab.x2[index],df_finalTab.y2[index])
            
            #cv2.imshow('Detected',image)
            #cv2.imwrite(r'D:\Study\Code\OCR_Invoice\Setup\rect.png', image)
            def drawRectangleValue(text,x1,y1,x2,y2):
                cv2.rectangle(image,(x1,y1) , (x1+x2,y1+y2), (0,100,0),1)
                return 
            drawRectangleValue('text',x1,y1,x2,y2)
            
            #cv2.imshow('Detected',image)
            cv2.imwrite(r'D:\Study\Code\OCR_Invoice\Setup\rect.png', image) 
    return text


text=checkHorizontalVertical(string,horiFileName,vertiFileName,tabularFileName)

  

#--------------------------------------------------------------------------------------------

