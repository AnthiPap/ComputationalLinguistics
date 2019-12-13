
from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.bleu_score import SmoothingFunction
import argparse
import sys
import csv
from cube.api import Cube

cube=Cube(verbose=True)
cube.load("en")

def argparser():
    Argparser = argparse.ArgumentParser()
    Argparser.add_argument('--reference', type=str, help='Reference File')
    Argparser.add_argument('--candidate', type=str, help='Candidate file')

    args = Argparser.parse_args()
    return args
args = argparser()

reference = open(args.reference, 'r').readlines()
candidate = open(args.candidate, 'r').readlines()

with open('pos_r.txt', 'w') as out1, open('pos_h.txt', 'w')as out2:
    for sentences in reference:
        sentences=cube(sentences)
        for sentence in sentences:
            for entry in sentence:
                out1.write(entry.upos+"\t"+entry.attrs)
                out1.write('')
    for sentences in candidate:
        sentences=cube(sentences)
        for sentence in sentences:
            for entry in sentence:
                out2.write(entry.upos+"\t"+entry.attrs)
                out2.write('')

cc=SmoothingFunction()

with open('pos_r.txt', 'r') as f1, open('pos_h.txt', 'r')as f2:
    f1=f1.readlines()
    f2=f2.readlines()
    if len(f1) != len(f2):
        raise ValueError('The number of sentences in both files do not match.')

    score = 0.

    for i in range(len(f1)):
        score += sentence_bleu([f1[i].strip().split()], f2[i].strip().split(),smoothing_function=cc.method5)

score /= len(f1)
print("The bleu score is: "+str(score))


