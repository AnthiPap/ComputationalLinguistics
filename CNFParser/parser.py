"""
CKY algorithm from the "Natural Language Processing" course by Michael Collins
https://class.coursera.org/nlangp-001/class
"""
import sys
from sys import stdin, stderr
from time import time
from json import dumps

from collections import defaultdict
from pprint import pprint

from pcfg import PCFG
from tokenizer import PennTreebankTokenizer

def argmax(lst):
    return max(lst) if lst else (0.0, None)

def backtrace(back, bp):
    if back==None: 
        return None
    elif len(back) == 2: #binary
        return list(back)
    else:
        lh=back[0] #non- terminals
        subt1=back[1] #this and the following are for subtrees
        subt2=back[2]
        minp=back[3]#the final three are the min, mid and max points.
        midp=back[4]
        maxp=back[5]

        return list((lh, backtrace(bp[(minp, midp, subt1)], bp), backtrace(bp[(midp, maxp, subt2)], bp)))
    


def CKY(pcfg, norm_words):
    ch = defaultdict(float) #score chart
    bp = defaultdict(tuple) #backpointers chart
    l=len(norm_words)

    for x in range(0, l): #for loop to add the words to the chart
        for (s,w) in pcfg.q1:
            if w== norm_words[x][0]:
                ch[(x, x+1, s)]=pcfg.q1[s,w]
                bp[(x, x+1, s)]= (s, norm_words[x][1])               
                
    
    for y in range(2, l+1): #dynamic programming part of the code, iteration over the rows
        for j in range(y, -1,-1):
            for n in pcfg.N:
                bestcand=0
                backpointer=0
                for rule in pcfg.binary_rules[n]:
                    for i in range(j+1, y):
                        r0=rule[0]
                        r1=rule[1]
                        if ch[(j, i, r0)]:
                            if ch[(i, y, r1)]:
                                t1=ch[(j, i, r0)]
                                t2=ch[(i,y,r1)]
                                cand=t1 * t2 *pcfg.q2[n, r0, r1]

                                if cand > bestcand:
                                    bestcand=cand
                                    backpointer=(n, r0, r1, j, i, y)
                if bestcand != 0:
                    ch[(j, y, n)]=bestcand
                    bp[(j, y, n)]=backpointer                  
                
    return backtrace(bp[0, l, "S"], bp) #assumption that we want trees with the "S" category

class Parser:
    def __init__(self, pcfg):
        self.pcfg = pcfg
        self.tokenizer = PennTreebankTokenizer()
    
    def parse(self, sentence):
        words = self.tokenizer.tokenize(sentence)
        norm_words = []
        for word in words:                # rare words normalization + keep word
            norm_words.append((self.pcfg.norm_word(word), word))
        tree = CKY(self.pcfg, norm_words)
        tree[0] = tree[0].split("|")[0]
        return tree
    
def display_tree(tree):
    pprint(tree)

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("usage: python3 parser.py GRAMMAR")
        exit()

    start = time()
    grammar_file = sys.argv[1]
    print("Loading grammar from " + grammar_file + " ...", file=stderr)    
    pcfg = PCFG()
    pcfg.load_model(grammar_file)
    parser = Parser(pcfg)

    print("Parsing sentences ...", file=stderr)
    for sentence in stdin:
        tree = parser.parse(sentence)
        print(dumps(tree))
    print("Time: (%.2f)s\n" % (time() - start), file=stderr)
