# -*- coding: utf-8 -*-
"""
Created on Thu Dec 08 02:39:58 2016

BM25 with Stemming
@author: Aditya C Awalkar
"""

import glob
import ast
import collections


# BM25 parameters.
from math import log

k1 = 1.2
k2 = 100
b = 0.75
avdl=0
N=3204

import pandas

def score_BM25(n, f, qf, r, K ,R):
	first = log( ( (r + 0.5) / (R - r + 0.5) ) / ( (n - r + 0.5) / (N - n - R + r + 0.5)) )
	second = ((k1 + 1) * f) / (K + f)
	third = ((k2+1) * qf) / (k2 + qf)
	return first * second * third


def compute_K(dlavdl):
	return k1 * ((1-b) + b * dlavdl )
 
 
#Store the stemmed version of corpus into dictionary
 
pre= 'CACM-'
corpus_dict={(pre + "%04d"%(k+1)):[] for k in range(3204)}

with open('cacm_stem.txt') as f:
    i=0;    
    for line in f:
        flag=0;
        l= line.strip()
        if l.startswith('#'):
            i+=1;
        if not l.startswith('#'):
            corpus_dict[pre + "%04d"%i]+=l.split() 



#Inverted Index
inv_index=dict()
for key in corpus_dict:
    c= collections.Counter()
    for value in corpus_dict[key]:
        c[value]+=1
    for value in c:
        if value not in inv_index:
            inv_index[value]=[(key,c[value])]
        else:
            inv_index[value].append((key,c[value]))
            
#print inv_index
            
#Document Frequency
doc_freq=dict()
for key in inv_index:
    df= len(inv_index[key]);
    doc_freq[key]=df;     



#Terms occuring in Which Documents 
term_dict=dict()           
for term,values in inv_index.iteritems():
    doc_list=[]    
    #t_list= ast.literal_eval('[{0}]'.format(x[1]));   
    for d in values:
        doc_list.append(d[0]);
    
    term_dict[term]= doc_list
       

        
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
        self.doc_name = document
        self.freq={}
        self.K=0;
        self.doc_len = doc_len
        self.initialize()

    def initialize(self):
        #print self.document;
        self.freq= {}
        for word in corpus_dict[self.document]:
                if word not in self.freq:
                    self.freq[word] = 0
                self.freq[word] += 1
        #print self.freq

        
        self.K = compute_K(float(self.doc_len)/float(avdl))







#Avdl calculation
total_doc_len=0
dl= dict()
for docs in corpus_dict:
    dl[docs] = len(corpus_dict[docs]); 
    total_doc_len+= dl[docs]
avdl= 1.0 * total_doc_len/ N;


obj_list = []
for docs in corpus_dict:
    bm25= BM25(docs,dl[docs]);
    obj_list.append(bm25);
    



#Query Input
queries=dict()
with open('cacm_stem_query.txt') as f:
    for line in f:
        print line
        query=line.strip().split('->');
        queries[query[0]]= query[1].strip().lower().split();


final_p= pandas.DataFrame(index=range(1),\
                          columns=['queryid','Q0','docid','rank','score','sys_name'])
ii=0


for qid,query_value in queries.iteritems():
    
    query_terms=dict()    
    
    
    #Calculate qf    
    for q in query_value:
        if q in query_terms:
            query_terms[q]+=1
        else:
            query_terms[q]=1

    #Calculate R
    #print qid
    #print rel_dict[str(qid)]
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
            
            
            #Calculate BM25 score for (term,doc)        
            sum_query += score_BM25(n,f,qf,r,K ,R)
            #print sum_query
            #print qid
        #break;
        doc_score_dict[doc.doc_name]=sum_query
    scored_list = sorted(doc_score_dict.iteritems(), key=lambda x:-x[1])[:100]
    #print scored_list
    #print qid
    p= pandas.DataFrame(scored_list, columns=['docid','score'])
    p['queryid']=int(qid)
    p['Q0']='Q0'
    p['rank']= p.index + 1
    p['sys_name']='BM25'
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
final_p.to_csv('BM25_stemming_low.txt',index=False, sep=' ');

    


            
            