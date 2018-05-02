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
from textblob import TextBlob

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
        from nltk.stem.porter import PorterStemmer
        ps=PorterStemmer()
        reviews=str(reviews).split()
        reviews=[ps.stem(word) for word in reviews if not word in set(stopwords.words('english'))]
        #reviews=[word for word in reviews if not word in set(stopwords.words('english'))]
        reviews=" ".join(reviews)
        corpus.append(reviews)
    return corpus

corpus=removeStopwordsJoin(summary)

#Text Blob +ve,-ve
def getSentiment(corpus,summary):
    review=[]
    for i in range(0,20):
        text=corpus[i]
        blob = TextBlob(text)
        polarity=blob.sentiment.polarity
        if(polarity>=0.1):
            polarity_sentiment="Positive"
        elif(polarity<=-0.1):
            polarity_sentiment="Negative"
        else:
            polarity_sentiment="Neutral"
        print(polarity_sentiment,blob.sentiment.polarity)
        review.append({
                "Summary":summary[i],
                #"Summary":corpus[i],
                "Sentiment":polarity_sentiment})
    return review

review=getSentiment(corpus,summary)