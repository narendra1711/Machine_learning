import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

#But the Naive Bayes classifier, especially in the Nltk library, 
#expects the input to be in this format: Every word must be followed by true. 
#So for example, if you have these words
"Hello World"
{'Hello': True,  'World': True}

# This is how the Naive Bayes classifier expects the input
def create_word_features(words):
    useful_words = [word for word in words if word not in stopwords.words("english")]
    my_dict = dict([(word, True) for word in useful_words])
    return my_dict

create_word_features(["the", "quick", "brown", "quick", "a", "fox"])

#Remember, the sentiment analysis code is just a machine learning algorithm that has been trained to identify positive/negative reviews.
neg_reviews = []
for fileid in movie_reviews.fileids('neg'):
#We create an empty list called neg_reviews. Next, we loop over all the files in the neg folder    
    words = movie_reviews.words(fileid)
#We get all the words in that file.
    neg_reviews.append((create_word_features(words), "negative"))
#Then we use the function we wrote earlier to create word features in the format nltk expects. 
    print(neg_reviews[0])    
    print(len(neg_reviews))    