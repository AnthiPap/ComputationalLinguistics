import nltk
import ast
import string
import re
import csv
import textblob
import itertools
from textblob import TextBlob
from textblob import Word
from textblob.classifiers import NaiveBayesClassifier
from nltk.corpus import twitter_samples
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wd
from nltk.tokenize import word_tokenize
from random import shuffle
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_recall_fscore_support as score
from gold_standard import y_true
from autocorrect import spell



stopwords = stopwords.words('english')
lemmatizer = nltk.WordNetLemmatizer().lemmatize
punct=['"','$','%','&','\',''','(',')','+',',','-','.','/',':',';','<','=','>','@','[','\',','^','_','`','{','|','}','~']

emoticons_happy = set([
    ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
    ':^)', ':-D', ':D', ': D','8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
    '=-3', '=3', ':-))', ':-)', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
    '<3',':*', ':p'
    ])

emoticons_sad = set([
    ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
    ':-[', ':-<', '=\\', '=/', '>:(', ':-(', '>.<', ":'-(", ":'(", ':\\', ':-c',
    ':c', ':{', '>:\\', ';('
    ])
emoticons = emoticons_happy.union(emoticons_sad)

    
def pre_process(tweet):

    tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet) #url removal
    
    tweet = re.sub(r'#', '', tweet) #hashtag removal, but keep text

    tweet=''.join([i for i in tweet if not i.isdigit()])#number removal
    
    tweet=re.sub(r'([.,/#!$%^&*;:{}=_`~-])([.,/#!$%^&*;:{}=_`~-]+)\1+', r'\1',tweet) #consecutive punc removal
    
    tweet = re.sub(r'@[A-Za-z0-9]+', '', tweet) #mention removal
    
    tweet=''.join([i for i in tweet if i not in emoticons]) #emoticon removal

    tweet=''.join([i for i in tweet if i not in punct]) #punctuation removal

    tweet=' '.join([i for i in tweet.split() if i not in stopwords]) #stopword removal

    tweet=tweet.lower() #lowercasing

    tweet=lemmatize(tweet) #lemmatizing

    return tweet


#the two functions below are to ensure that not only nouns (default) are lemmatized
def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wd.ADJ
    elif treebank_tag.startswith('V'):
        return wd.VERB
    elif treebank_tag.startswith('N'):
        return wd.NOUN
    elif treebank_tag.startswith('R'):
        return wd.ADV
    else:
        return wd.NOUN

def lemmatize(tt):
    pos = nltk.pos_tag(nltk.word_tokenize(tt))
    lemm = [lemmatizer(sw[0], get_wordnet_pos(sw[1])) for sw in pos]
    sentence= ' '.join([i for i in lemm])

    return sentence


test_tweets=[]
file=open('scraped_tweets.csv', 'r')
reader = csv.reader(file)
for line in reader:
    line=line[1]
    test_tweets.append(line)
    
pos_tweets = twitter_samples.strings('positive_tweets.json')
neg_tweets = twitter_samples.strings('negative_tweets.json')


proc_train_pos=[]
for tweet in pos_tweets:
    proc_train_pos.append(pre_process(tweet))
proc_train_neg=[]
for tweet in neg_tweets:
    proc_train_neg.append(pre_process(tweet))
test=[]
for tweet in test_tweets:
    test.append(pre_process(tweet))

proc_test=[]
#some extra pre-processing for the test set
for tweet in test:
    clean=tweet.replace("b'", '').replace("b '", '').replace('b"','').replace("amp", "and")
    clean2=re.sub(r'\\n', '', clean)
    clean3=re.sub(r'\\x?\w', '', clean2)
    #clean4=' '.join([spell(word) for word in clean3.split()]) #spell check
    proc_test.append(clean3)

#feature extraction
def bag_of_words(tweet):
    words_dictionary = dict([word, True] for word in tweet.split())    
    return words_dictionary


pos_tweets_set = []
for tweet in proc_train_pos:
    pos_tweets_set.append((bag_of_words(tweet), 'pos'))
 
neg_tweets_set = []
for tweet in proc_train_neg:
    neg_tweets_set.append((bag_of_words(tweet), 'neg'))


#shuffle to get random order of pos/neg
shuffle(pos_tweets_set)
shuffle(neg_tweets_set)
train_set = pos_tweets_set+neg_tweets_set

print('Training begins ')

classifier = NaiveBayesClassifier(train_set)

print('Training is done ')

y_predicted = [classifier.classify(bag_of_words(tweet)) for tweet in proc_test] #testing

#evaluation
accuracy = accuracy_score(y_true, y_predicted)
print('Accuracy for Naive Bayes is : ',accuracy, '\n')

precision, recall, fscore, support = score(y_true, y_predicted)

print('Precision for Naive Bayes is : ', precision, '(neg // pos)')
print('Recall for Naive Bayes is : ',recall, '(neg // pos)')
print('F-measure for Naive Bayes is : ',fscore, '(neg // pos)''\n')

precision, recall, fscore, support = score(y_true, y_predicted, average='weighted')

print('Weighted Precision for Naive Bayes is : ', precision)
print('Weighted Recall for Naive Bayes is : ',recall)
print('Weighted F-measure for Naive Bayes is : ',fscore, '\n')

from sklearn.metrics import confusion_matrix

tn, fp, fn, tp = confusion_matrix(y_true, y_predicted).ravel()
print('True Negatives were ',tn)
print('False Positives were ',fp)
print('False Negatives were ',fn)
print('True Positives were ',tp,'\n')

from sklearn.metrics import classification_report

print(classification_report(y_true, y_predicted))

