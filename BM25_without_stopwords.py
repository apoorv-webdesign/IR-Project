# -*- coding: utf-8 -*-
"""
Created on Tue Dec 06 19:14:12 2016

BM25 without stopwords
@author: Aditya C Awalkar
"""

import glob
import ast
import pandas


# BM25 parameters.
from math import log

k1 = 1.2
k2 = 100
b = 0.75
avdl=0
N=3204


def score_BM25(n, f, qf, r, K ,R):
	first = log( ( (r + 0.5) / (R - r + 0.5) ) / ( (n - r + 0.5) / (N - n - R + r + 0.5)) )
	second = ((k1 + 1) * f) / (K + f)
	third = ((k2+1) * qf) / (k2 + qf)
	return first * second * third


def compute_K(dlavdl):
	return k1 * ((1-b) + b * dlavdl )
 
 
 
#Term occurs in which documents Computation      
inv_index= []      
with open('unigram_index.txt') as f2:
    for line in f2:
        x=line.strip().split('->');
        #print x[0]
        inv_index.append(line.strip());
 
 
#Terms occuring in Which Documents 
term_dict=dict()           
for t in inv_index:
    doc_list=[]
    x=t.strip().split('->');
    term= x[0].strip();
    t_list= ast.literal_eval('[{0}]'.format(x[1]));   
    for d in t_list:
        doc_list.append(d[0]);
    
    term_dict[term]= doc_list
             
 
 
doc_freq = dict()
with open('doc_frequency.txt') as f:
    for line in f:
        term= line.strip().split(' -> ')
        doc_freq[term[0]]= term[1]  
        

#Relevance Calculation
rel_dict ={str((k+1)):[] for k in range(64)};

with open('cacm.rel') as f:
    for line in f:
        entry= line.strip().split()
        qid= entry[0]
        docid = entry[2]
        rel_dict[qid].append(docid);


class BM25(object):

    def __init__(self, document, doc_len):
        self.document= document        
        self.doc_name = document.split("tok\\")[1].split('.txt')[0]
        self.freq={}
        self.K=0;
        self.doc_len = doc_len
        self.initialize()

    def initialize(self):
        #print self.document;
        self.freq= {}
        with open(self.document) as f:        
            for word in f:
                sword= word.strip()
                if sword not in self.freq:
                    self.freq[sword] = 0
                self.freq[sword] += 1
        #print self.freq

        
        self.K = compute_K(float(self.doc_len)/float(avdl))


#Avdl calculation
total_doc_len=0
dl= dict()
for docs in glob.glob('cacm_tok\*.txt'):
    dl[docs] = sum(1 for line in docs); 
    total_doc_len+= dl[docs]
avdl= 1.0 * total_doc_len/ N;


corpus = glob.glob('cacm_tok\*.txt');  

obj_list = []
for docs in corpus:
    bm25= BM25(docs,dl[docs]);
    obj_list.append(bm25);
    

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

final_p= pandas.DataFrame(index=range(1),\
                          columns=['queryid','Q0','docid','rank','score','sys_name'])
ii=0


for qid,query_val in queries.iteritems():
    query_value= query_val.split(' ');    
    query_terms=dict()    
    
    
    #Calculate qf    
    for q in query_value:
        
        #Remove Stopwords
        if q not in stopwords: 
            if q in query_terms:
                query_terms[q]+=1
            else:
                query_terms[q]=1
    #Calculate R
    R= len(rel_dict[str(qid)])
    
    doc_score_dict=dict()    
    
    for doc in obj_list:    
        sum_query=0;
        for term in query_terms:
            
            #n Calculation            
            if term in doc_freq:            
                n= int(doc_freq[term])
            else:
                n=0;
                
            #print doc.f
            
            #f Calculation    
            if term in doc.freq:
                f= int(doc.freq[term])
            else:
                f=0
            qf= query_terms[term]
            K= doc.K
            r=0;
            
            #Check relevance information for this term
            for value in rel_dict[qid]:
                if term in term_dict:                
                    if value in term_dict[term]:                
                        r+=1;
            """
            print term, type(term)
            print n, type(n)
            print f, type(f)
            print qf, type(qf)
            print K, type(K)
            print R, type(R)
            """
            #Calculate BM25 score for (term,doc)        
            sum_query += score_BM25(n,f,qf,r,K ,R)
            #print sum_query
            #print qid
        #break;
        doc_score_dict[doc.doc_name]=sum_query
    scored_list = sorted(doc_score_dict.iteritems(), key=lambda x:-x[1])[:100]
    #print scored_list
    
    #break;
    
    p= pandas.DataFrame(scored_list, columns=['docid','score'])
    p['queryid']=int(qid)
    p['Q0']='Q0'
    p['rank']= p.index + 1
    p['sys_name']='BM25_stopping'
    #print p
    p_reorder= p[['queryid','Q0','docid','rank','score','sys_name']]
    #p_reorder.columns = range(p_reorder.shape[1])
    #print p_reorder
    final_p= final_p.append(p_reorder)
    #print final_p
    ii+=1;
    print ii;
    #if ii==3:
        
        #break;
#final_p.drop(0,inplace=True)
final_p= final_p[final_p.docid.notnull()]
print final_p    



final_p.sort_values(['queryid','rank'],inplace=True)
#print final_p    

#write to CSV
final_p.to_csv('BM25_stopping_low.txt',index=False, sep=' ');


      

            
            