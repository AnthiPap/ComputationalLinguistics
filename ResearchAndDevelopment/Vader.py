import nltk
import ast
import re
import csv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import string
import textblob
from nltk.corpus import wordnet as wd
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_recall_fscore_support as score
from autocorrect import spell
from gold_standard import y_true


vader = SentimentIntensityAnalyzer()
    
def pre_process(tweet):
    
    tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet) #url removal
    tweet = re.sub(r'#', '', tweet) #hashtag removal, but keep text
    tweet=''.join([i for i in tweet if not i.isdigit()]) #number removal
    tweet = re.sub(r'@[A-Za-z0-9]+', '', tweet) #mention removal
    tweet= tweet.replace("b'", '').replace("b '", '').replace('b"','').replace("amp", "and")
    tweet= re.sub(r'\\n', '', tweet)
    tweet=re.sub(r'\\x?\w', '', tweet)
    #tweet= ' '.join([spell(word) for word in tweet.split()]) #spell checking
    
    return tweet


test_tweets=[]
file=open('scraped_tweets.csv', 'r')
reader = csv.reader(file)
for line in reader:
    line=line[1]
    test_tweets.append(line)
    
proc_test=[]
for tweet in test_tweets:
    proc_test.append(pre_process(tweet))


def vader_polarity(text):
    score = vader.polarity_scores(text)
    return 'pos' if score['pos'] > score['neg'] else 'neg'
            
y_predicted=[vader_polarity(tweet) for tweet in proc_test]

#evaluation
accuracy = accuracy_score(y_true, y_predicted)
print('Accuracy for VADER is : ',accuracy, '\n')

precision, recall, fscore, support = score(y_true, y_predicted)

print('Precision for VADER  is : ', precision, '(neg // pos)')
print('Recall for VADER  is : ',recall, '(neg // pos)')
print('F-measure for VADER  is : ',fscore, '(neg // pos)''\n')

precision, recall, fscore, support = score(y_true, y_predicted, average='weighted')

print('Weighted Precision for VADER  is : ', precision)
print('Weighted Recall for VADER is : ',recall)
print('Weighted F-measure for  : ',fscore, '\n')

from sklearn.metrics import confusion_matrix

tn, fp, fn, tp = confusion_matrix(y_true, y_predicted).ravel()
print('True Negatives were ',tn)
print('False Positives were ',fp)
print('False Negatives were ',fn)
print('True Positives were ',tp,'\n')

from sklearn.metrics import classification_report

print(classification_report(y_true, y_predicted))

