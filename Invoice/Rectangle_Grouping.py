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

#Convert word_infos dictionary to Dataframe and converts boundaries to 4 individual columns x1,y1,x2,y2
df=pd.DataFrame(word_infos)
df = df.join(pd.DataFrame(df['boundingBox'].str.split(',').tolist(),columns = ['x1','y1','x2','y2']))
del df['boundingBox']
df.x1 = df.x1.astype(np.int64)
df.y1 = df.y1.astype(np.int64)
df.x2 = df.x2.astype(np.int64)
df.y2 = df.y2.astype(np.int64)


image_path=r"D:\Study\GitHub\Machine_learning\Invoice\pic.jpg"
image=cv2.imread(image_path)

def drawRectangle(text,x1,y1,x2,y2):
    cv2.rectangle(image,(x1,y1) , (x1+x2,y1+y2), (0,0,255),1)
    return

for i in range(0,len(word_infos)):
    drawRectangle(df['text'][i],df['x1'][i],df['y1'][i],df['x2'][i],df['y2'][i])

'''cv2.imshow('Detected',image)
cv2.waitKey(0)
cv2.destroyAllWindows() '''

keys=['LLC','BILL']
index=[]
for i in range(0,len(df)):
    for j in range(0,len(keys)):
        if(df.text[i]==keys[j]):
            if(j==len(keys)-1):
                index.append(i-1)
            else:
                index.append(i+1)
elements=[]            
for i in range(0,len(index)-1):
    elements.append(df[index[i]:index[i+1]+1])

max=0
elements[0]['X']=elements[0]['x1']+elements[0]['x2']

    
x1=elements[0]['x1'].iloc[0]
y1=elements[0]['y1'].iloc[0]
x2=elements[0]['X'].max()
y2=elements[0]['y2'].iloc[len(elements[0])-1]+elements[0]['y1'].iloc[len(elements[0])-1]
   
print(x1,y1,x2,y2) 

image_path=r"D:\Study\GitHub\Machine_learning\Invoice\pic.jpg"
image=cv2.imread(image_path)

cv2.rectangle(image,(x1,y1) , (x2,y2), (0,0,255),1)    
cv2.imshow('Detected',image)
cv2.waitKey(0)
cv2.destroyAllWindows()      
        
        
        