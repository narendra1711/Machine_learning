# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 12:01:14 2018

@author: Narendra_Mugada
"""
from nltk.corpus import inaugural
from wordcloud import WordCloud
import matplotlib.pyplot as plt
text=["hello how are you","hello iam good"]
words=[]
for i in range(0,len(text)):
    text[i]=text[i].split()
    for j in range(0,len(text[i])):
        words.append(text[i][j])
        
text=str(words).replace("'","")
wordcloud = WordCloud(max_font_size=50).generate(text)
plt.figure(figsize=(6,3))
# plot wordcloud in matplotlib
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()