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

image_path=r"D:\Project\pic.jpg"
image=cv2.imread(image_path)
def drawRectangle(text,x1,y1,x2,y2):
    cv2.rectangle(image,(x1,y1) , (x1+x2,y1+y2), (0,0,255),1)
    return

for i in range(0,len(word_infos)):
    drawRectangle(df['text'][i],df['x1'][i],df['y1'][i],df['x2'][i],df['y2'][i])

#This part displays input image with all Rectangles for given boundaries in dataframe
#cv2.imwrite(r'D:\WorkArea\Code\Invoice\pics\pics\Phase-1\velimark-2.jpg', image)

#keys=['Vendor','address','Please','deliver','to:','Purchase','Order','Ordering','Terms','of','Payment','PO','Number','Date','Contact','Person','Our','VAT','Registration','No.']

keys=['Ordering','address']
kw=[]
d={}
for i in range(0 , len(df)):
    for j in range(0 , len(keys)):
        if df['text'][i]==keys[j]:
            d={'text':df['text'][i],
               'x1':df['x1'][i],
               'y1':df['y1'][i],
               'x2':df['x2'][i],
               'y2':df['y2'][i]}
            kw.append(d)

final_dict={}
sub_dict={}
final=[]

for i in range(0,len(kw)-1):
    if(kw[i]['y1']==kw[i+1]['y1']):
        sub_dict=kw[i],kw[i+1]
        

image_path=r"D:\Project\pic.jpg"
image=cv2.imread(image_path)
def drawRectangle(text,x1,y1,x2,y2):
    cv2.rectangle(image,(x1,y1) , (x1+x2,y1+y2), (0,0,255),1)
    return

for i in range(0,len(final)):
    drawRectangle(final[i]['final_text'],final[i]['x1'],final[i]['y1'],final[i]['x2'],final[i]['y2'])
#drawRectangle("Vendor",67,411,117,13)

#This part displays input image with all Rectangles for given boundaries in dataframe
#cv2.imwrite(r'D:\WorkArea\Code\Invoice\pics\pics\Phase-1\velimark-2.jpg', image)
  

final_dict={}
final=[]
df_kw=pd.DataFrame(kw)
a=df_kw.groupby('y1')


for i in a:
    c=[]
    b=""
    for j in range(0,(len(i[1]))):
       #print (i[1]['text'].iloc[j])
       x1=y1=x2=y2=0
       b=' '.join([b,i[1]['text'].iloc[j]])
       x1=i[1]['x1'].iloc[0]
       x2=i[1]['x2'].iloc[len(i[1])-1]+i[1]['x1'].iloc[len(i[1])-1]-i[1]['x1'].iloc[0]
       y1=i[1]['y1'].iloc[0]
       y2=i[1]['y2'].iloc[len(i[1])-1]
    c.append(b) 
    print (c)
    final_dict={"text":c,"x1":x1,"x2":x2,"y1":y1,"y2":y2}
    final.append(final_dict)


for i in range(0,len(final)):
    drawRectangle(final[i]['text'],final[i]['x1'],final[i]['y1'],final[i]['x2'],final[i]['y2'])
cv2.imshow('Detected',image)
cv2.waitKey(0)
cv2.destroyAllWindows()    

