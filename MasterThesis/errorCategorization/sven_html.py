import numpy
import argparse
from error_categorization import incorrect


def argparser():
    Argparser = argparse.ArgumentParser()
    Argparser.add_argument('--reference', type=str, default='summaries.txt', help='Reference File')
    Argparser.add_argument('--candidate', type=str, default='candidates.txt', help='Candidate file')

    args = Argparser.parse_args()
    return args

args = argparser()

reference = open(args.reference, 'r').readlines()
hypothesis = open(args.candidate, 'r').readlines()

def wer(r, h):
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


    x = len(r)
    y = len(h)

    html = '<html><body><head><meta charset="utf-8"></head>' \
           '<style>.g{background-color:#0080004d}</style><br><br>'

    wordList=incorrect
    while True:
        if x == 0 or y == 0:
            break

        if r[x - 1] == h[y - 1]:
            x = x - 1
            y = y - 1
            html = '%s ' % h[y] + html
        elif d[x][y] == d[x - 1][y - 1] + 1:    # substitution
            x = x - 1
            y = y - 1
            if r[x] in wordList:
                html = '<span class="g">(%s)</span> ' % (r[x]) + html
            html='%s ' % h[y] + html

        elif d[x][y] == d[x - 1][y] + 1:        # deletion r
            x = x - 1
            if r[x]==i:
                html = '<span class="g">(%s)</span> ' % (r[x]) + html
                 
            html='%s ' % h[y] + html
        elif d[x][y] == d[x][y - 1] + 1:        # insertion h
            y = y - 1
            if r[x]==i:
                html = '<span class="g">(%s)</span> ' % (r[x]) + html
                 
            html='%s ' % h[y] + html
        else:
            print('Error.')
            break

    html = html + '</body></html>'

    return html

with open('diff.html', 'w', encoding='utf8') as f:
    l=[]
    for i, j in zip(reference,hypothesis):
        i=i.split()
        j=j.split()
        l.append(wer(i,j))
    for el in l:
        f.write(el+'\n')
            
