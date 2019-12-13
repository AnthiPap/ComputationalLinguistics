import numpy
from nltk import word_tokenize
from cube.api import Cube
import argparse
from tabulate import tabulate

cube=Cube(verbose=True)
cube.load('en')


def argparser():
    Argparser = argparse.ArgumentParser()
    Argparser.add_argument('--reference', type=str, help='Reference File')
    Argparser.add_argument('--candidate', type=str, help='Candidate file')

    args = Argparser.parse_args()
    return args
args = argparser()

ref = open(args.reference, 'r').read().split()
hyp = open(args.candidate, 'r').read().split()


##### WER
def edit(r, h):
    d = numpy.zeros((len(r) + 1) * (len(h) + 1), dtype=numpy.uint16)
    d = d.reshape((len(r) + 1, len(h) + 1))
    for i in range(len(r) + 1):
        for j in range(len(h) + 1):
            if i == 0:
                d[0][j] = j
            elif j == 0:
                d[i][0] = i

    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            if r[i - 1] == h[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                substitution = d[i - 1][j - 1] + 1
                insertion = d[i][j - 1] + 1
                deletion = d[i - 1][j] + 1
                d[i][j] = min(substitution, insertion, deletion)
    return d
    

def getStepList(r, h, d):
    x = len(r)
    y = len(h)
    insertions=[]
    substitutions=[]
    deletions=[]
    while True:
        if x == 0 or y == 0:
            break
        if r[x-1] == h[y-1]:
            x = x - 1
            y = y - 1
        elif d[x][y] == d[x][y-1]+1:
            #insertion
            y = y - 1
            insertions.append(h[y])
        elif d[x][y] == d[x-1][y-1]+1:
            #substitution
            x = x - 1
            y = y - 1
            substitutions.append(r[x])
        elif d[x][y] == d[x-1][y] + 1:
            #deletion
            x = x - 1
            deletions.append(r[x])
        else:
            print('Error')
            break

    return insertions, substitutions, deletions

def wer(r, h):
    d = edit(r, h)
    a= getStepList(r, h, d)
    return a




##### PER and, RPER HPER and FPER
hyp_errors=[]
hyp_errors.append(set(hyp)-set(ref))
hyp_errors=[item for sublist in hyp_errors for item in sublist]
ref_errors=[]
ref_errors.append(set(ref)-set(hyp))
ref_errors = [item for sublist in ref_errors for item in sublist]

#RPER=len(ref_errors)/len(word_tokenize(ref))
#HPER=len(hyp_errors)/len(word_tokenize(hyp))
#FPER=(len(ref_errors)+len(hyp_errors))/(len(word_tokenize(ref))+len(word_tokenize(hyp)))

all_errors=[]
##### Inflectional Errors
# If there are lemmarized words in the hypothesis that match a word in the reference sentence. e.g. 'is'

d=dict()
for i in hyp_errors:
    q=cube(i)
    for entry in q:
        for t in entry:
           d[i]=t.lemma

def getKeysByValues(dictOfElements, listOfValues):
    listOfKeys = list()
    listOfItems = dictOfElements.items()
    for item  in listOfItems:
        if item[1] in listOfValues:
            listOfKeys.append(item[0])
    return  listOfKeys
infl= getKeysByValues(d, ref_errors)
all_errors.append(infl)

##### Reordering Errors
# For this we are going to first take all words which are present both in the hypothesis
# and the reference, and then check if they were also marked as a WER error. e.g. 'sometimes'

all_r=[]
all_h=[]
for i in ref:
    i=cube(i)
    for sentence in i:
        for entry in sentence:
            all_r.append(entry.word)
for j in hyp:
    j=cube(j)
    for sentence in j:
        for entry in sentence:
            all_h.append(entry.word)
all_final=list(set(all_r).intersection(all_h))
werr=wer(ref,hyp)
flat_wer=[item for sublist in werr for item in sublist]
reorder=list(set(flat_wer).intersection(all_final))



##### Missing words
# Errors present in the deletion list of the WER algorithm, which are also present as RPER errors
# but do not share the same base form as any errors present as HPER errors. eg.'can'

del_e=werr[2]
first=list(set(del_e).intersection(ref_errors))

lemma_d=[]
lemma_hyp=[]
for i in first:
    i=cube(i)
    for entry in i:
        for j in entry:
            lemma_d.append(j.lemma)
for j in hyp:
    j=cube(j)
    for entry in j:
        for x in entry:
            lemma_hyp.append(x.lemma)
            
missing=list(set(lemma_d)-set(lemma_hyp))
all_errors.append(missing)

##### Extra words
# Errors present in the insertion list of the WER algorithm, which are also present as HPER errors
# but do not share the same base form as any errors present as RPER errors. []

extra= wer(ref,hyp)[0] 

first=list(set(extra).intersection(hyp_errors))

lemma=[]
for i in first:
    i=cube(i)
    for entry in i:
        for j in entry:
            lemma.append(j.lemma)

            
extra_w=list(set(first)-set(lemma))


##### Incorrect lexical choice
# errors in the reference that do not fall in the category of either an inflectional, or missing error. e.g. 'Mrs' or 'Mister'
all_errors_f=[item for sublist in all_errors for item in sublist]

lemma_i=[]
for i in all_errors_f:
    i=cube(i)
    for entry in i:
        for j in entry:
            lemma_i.append(j.lemma)

incorrect=list(set(ref_errors)-set(lemma_i))


table=tabulate([['Inflectional errors', len(infl)], ['Reordering errors', len(reorder)],['Missing words', len(missing)],['Extra words', len(extra_w)],['Incorrect lexical choices', len(incorrect)]], headers=['Type of error', 'Number of errors'], tablefmt='orgtbl')
print(table) 
      





                         

