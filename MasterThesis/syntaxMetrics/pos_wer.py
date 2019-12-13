from nltk import word_tokenize
from cube.api import Cube
import numpy
import argparse
from tabulate import tabulate

cube=Cube(verbose=True)
cube.load("en")

def argparser():
	Argparser = argparse.ArgumentParser()
	Argparser.add_argument('--reference', type=str, default='summaries.txt', help='Reference File')
	Argparser.add_argument('--candidate', type=str, default='candidates.txt', help='Candidate file')

	args = Argparser.parse_args()
	return args

args = argparser()

reference = open(args.reference, 'r').read().split()
candidate = open(args.candidate, 'r').read().split()

ADJ=[]
ADP=[]
ADV=[]
AUX=[]
CCONJ=[]
DET=[]
INTJ=[]
NOUN=[]
NUM=[]
PART=[]
PRON=[]
PROPN=[]
PUNCT=[]
SCONJ=[]
SYM=[]
VERB=[]
X=[]

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
    list = []
    while True:
        if x == 0 or y == 0:
            break
        if r[x-1] == h[y-1]:

            y = y - 1
        elif d[x][y] == d[x][y-1]+1:
                #insertion
                y = y - 1
                list.append(h[y])

        elif d[x][y] == d[x-1][y-1]+1:
                #substitution
                x = x - 1
                y = y - 1
                list.append(r[x])

                
        elif d[x][y] == d[x - 1][y] + 1:
                #deletion
                x = x - 1
                list.append(r[x])

        else:
            print('Error')
            break

    return list[::-1]

def wer(r, h):
    d = edit(r, h)
    list = getStepList(r, h, d)
    return list


a=wer(reference, candidate)

all_upos=[]
for i in a:
	i=cube(i)
	for x in i:
		for y in x:
			all_upos.append(y.upos)
			

			

for i in all_upos:

    if i=='ADJ':
        ADJ.append(i)
    elif i=='ADP':
        ADP.append(i)
    elif i=='ADV':
        ADV.append(i)
    elif i=='AUX':
        AUX.append(i)
    elif i=='CCONJ':
        CCONJ.append(i)
    elif i=='DET':
        DET.append(i)
    elif i=='INTJ':
        INTJ.append(i)
    elif i=='NOUN':
        NOUN.append(i)
    elif i=='NUM':
        NUM.append(i)
    elif i=='PART':
        PART.append(i)
    elif i=='PRON':
        PRON.append(i)
    elif i=='PROPN':
        PROPN.append(i)
    elif i=='PUNCT':
        PUNCT.append(i)
    elif i=='SCONJ':
        SCONJ.append(i)
    elif i=='SYM':
        SYM.append(i)
    elif i=='DET':
        DET.append(i)
    elif i=='X':
        X.append(i)
    elif i=='VERB':
        VERB.append(i)
    else:
        print(i)
        

adj="{:.2%}".format(len(ADJ)/len(reference))
adp="{:.2%}".format(len(ADP)/len(reference))
adv="{:.2%}".format(len(ADV)/len(reference))
aux= "{:.2%}".format(len(AUX)/len(reference))
cconj="{:.2%}".format(len(CCONJ)/len(reference))
det= "{:.2%}".format(len(DET)/len(reference))
intj= "{:.2%}".format(len(INTJ)/len(reference))
noun= "{:.2%}".format(len(NOUN)/len(reference))
num= "{:.2%}".format(len(NUM)/len(reference))
part= "{:.2%}".format(len(PART)/len(reference))
pron= "{:.2%}".format(len(PRON)/len(reference))
propn= "{:.2%}".format(len(PROPN)/len(reference))
punct= "{:.2%}".format(len(PUNCT)/len(reference))
sconj= "{:.2%}".format(len(SCONJ)/len(reference))
sym= "{:.2%}".format(len(SYM)/len(reference))
verb= "{:.2%}".format(len(VERB)/len(reference))
x= "{:.2%}".format(len(X)/len(reference))

table=tabulate([['ADJ', adj], ['ADP', adp],['ADV', adv],['AUX', aux],['CCONJ', cconj],['DET', det],['INTJ', intj],['NOUN', noun],['NUM', num],
        ['PART', part],['PRON', pron],['PUNCT', punct],['SCONJ', sconj],['SYM', sym],['VERB', verb],['X', x]], headers=['POS-tag', 'WER percentage'], tablefmt='orgtbl')
print(table)


