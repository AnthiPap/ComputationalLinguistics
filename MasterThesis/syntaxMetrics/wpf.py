from cube.api import Cube
import argparse

cube=Cube(verbose=True)
cube.load("en")

r1=[]
r2=[]

h1=[]
h2=[]


def argparser():
	Argparser = argparse.ArgumentParser()
	Argparser.add_argument('--reference', type=str, default='summaries.txt', help='Reference File')
	Argparser.add_argument('--candidate', type=str, default='candidates.txt', help='Candidate file')

	args = Argparser.parse_args()
	return args

args = argparser()

reference = open(args.reference, 'r').readlines()
candidate = open(args.candidate, 'r').readlines()

for i in reference:
	i=cube(i)
	for el in i:
		for x in el:
			r1.append(x.word)
			r2.append(x.upos)
for i in candidate:
	i=cube(i)
	for el in i:
		for x in el:
			h1.append(x.word)
			h2.append(x.upos)

same_w=set(r1)&set(h1)
same_w_l=len(same_w) #use this

same_p=set(r2)&set(h2)
same_p_l=len(same_p) #use this

total_w= len(r1)+len(h1)
total_p=len(r2)+len(h2)
ref_w_l=len(r1)
ref_p_l=len(r2)

precision_word= same_w_l/total_w
recall_word=same_w_l/ref_w_l
f_word=(2*(precision_word*recall_word))/(precision_word+recall_word)

precision_pos=same_p_l/total_p
recall_pos=same_p_l/ref_p_l
f_pos=(2*(precision_pos*recall_pos))+(precision_pos+recall_pos)

total=(f_word+f_pos)/2
print("{:.3%}".format(total))


		
