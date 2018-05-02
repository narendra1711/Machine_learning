import feedparser as fp
from newspaper import Article
url="http://feeds.feedburner.com/ndtvnews-top-stories"

#Parse URL
def parseURL(url):
    return fp.parse(url)

parsed=parseURL(url)

#Get Summary of each article
def getSummary(parsed):
    summary=[]
    for i in range(0,20):   
        article=Article(parsed['entries'][i]['link'],language="en")
        article.download()
        article.parse()
        article.nlp()
        summary.append(article.summary)
    return summary

summary=getSummary(parsed)

import nltk
from nltk.corpus import stopwords
import re
#from textblob import TextBlob

def removeStopwordsJoin(summary):
    corpus=[]
    #Download stopwords packages
    nltk.download('stopwords')
    for item in range(0,20):
        #Reviews should contain only alphabets
        reviews=re.sub('[^a-zA-Z]',' ',str(summary[item]))
        #Convert reviews to lower-case
        reviews=reviews.lower()
        #Stem the word
        #from nltk.stem.porter import PorterStemmer
        #ps=PorterStemmer()
        reviews=str(reviews).split()
        reviews=[word for word in reviews if not word in set(stopwords.words('english'))]
        #reviews=[word for word in reviews if not word in set(stopwords.words('english'))]
        #reviews=" ".join(reviews)
        corpus.append(reviews)
    return corpus

corpus=removeStopwordsJoin(summary)

#from nltk.corpus import inaugural
from wordcloud import WordCloud
import matplotlib.pyplot as plt
#text=["hello how are you","hello iam good"]
words=[]
for i in range(0,len(corpus)):
    #corpus[i]=corpus[i].split()
    for j in range(0,len(corpus[i])):
        words.append(corpus[i][j])
        
text=str(words).replace("'","")
wordcloud = WordCloud(max_font_size=50).generate(text)
plt.figure(figsize=(6,3))
# plot wordcloud in matplotlib
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()