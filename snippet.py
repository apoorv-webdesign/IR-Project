# -*- coding: utf-8 -*-
"""
Created on Fri Dec 09 01:56:46 2016

Snippet Generation
@author: Aditya C Awalkar
"""

import pandas

BOLD = '\033[1m'
END = '\033[0m'

#For Query No 7
#Using Top 15 results retrived by BM25
test_qid= '7'


#Read Stopwords
stopwords=[]
with open('common_words.txt') as f:
    for line in f:
        stopwords.append(line.strip())    


#Query Input
queries=dict()
with open('queries_list.txt') as f:
    i=1    
    for line in f:
        query=line.strip();
        queries[str(i)]= query.lower();
        i+=1;

test_query= queries[test_qid]

#Unique words
query_unique=[]
words= test_query.strip().split()
for word in words:
    if word not in query_unique:
        query_unique.append(word);

bm25_result= pandas.read_csv('files\BM25.txt',sep=' ')
bm25_test_docs = bm25_result.loc[bm25_result['queryid']==int(test_qid),'docid'].head(15)

#print bm25_test
add= 'cacm_tok\\'
months=['january','february','march','april','may', 'june', 'july' \
        'august','september','october','november','december']


#Store the important content of the documents and discard the rest
content=dict()
for doc in bm25_test_docs:
    content[doc]=[]     
    with open(add+ doc +'.txt') as f:
       flag=0
       for line in f:
            if line.strip() not in months: 
                if flag==0:                            
                    content[doc].append(line.strip())
            else:
                flag=1;
                del content[doc][-1]
                
neighbour=3         
                
for doc in bm25_test_docs:                
    snippet=''    
    terms= query_unique;
    #print terms
    for term in terms:
        
        if term not in stopwords:
            #print term
            if term in content[doc]:
                found_i= content[doc].index(term)
            
                try:
                    #print term
                    #highlight= '*'+term +'*'
                    #content[doc][content[doc]==term]= highlight
                    found_i= content[doc].index(term)
                    start= max(found_i- neighbour+1,0)
                    end= min(found_i+ neighbour,len(content[doc]))
                    #print found_i
                    #print start
                    #print end
                    snippet= snippet+'\n'+ ' '.join(content[doc][start:end])
                    #print snippet
                except:
                    print "not possible"
    
    with open('files\snippet.txt','a') as f:
        f.write(snippet+ '\n')           