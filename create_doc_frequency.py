import glob
import os
import time
import sys
import re
import collections
from collections import defaultdict
from itertools import tee, islice

dict_unigram_index={}

def create_unigram_index(filename):
	f = open(filename, 'r')
	c= collections.Counter(ngrams(f,1))
	
	for k,v in c.iteritems():
		k=list(k)
		k=[each.rstrip('\n') for each in k]
		k=tuple(k)
		if k not in dict_unigram_index:
			dict_unigram_index[k]=[]
			dict_unigram_index[k].append((filename.split('\\', 1)[-1],v))
		else:
			dict_unigram_index[k].append((filename.split('\\', 1)[-1],v))
	f.close()

def ngrams(f,n):
	while True:
		first, second = tee(f)
		ngram = tuple(islice(first, n))
		if len(ngram) == n:
			yield ngram
			next(second)
			f = second
		else:
			break
	
def unigram_index():
	for filename in glob.glob('Corpus having Tokens\*.txt'):
		create_unigram_index(filename)
	with open("term_frequency.txt",'w') as input_file:
		for i,j in dict_unigram_index.iteritems():
			line=i[0]+' -> '+str(len(j))+'\n'
			input_file.write (line)

def main():
	unigram_index()
main()