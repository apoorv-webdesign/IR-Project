# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 17:11:14 2016

Task 2
@author: Aditya C Awalkar
"""

import glob
import ast
import pickle
import pandas
import numpy
import math


N=3204;
queries=[];
temp=[]
query_terms=dict();


#Query Input
queries=dict()
with open('queries_list.txt') as f:
    i=1    
    for line in f:
        query=line.strip();
        queries[str(i)]= query.lower();
        i+=1;


for qid,query in queries.iteritems():
    s=query.split();
    for k in s:    
        if k not in temp:
            temp.append(k);
            
query_terms= {k:0 for k in temp}
#query_terms=set(query_terms);


k=[];
for file in glob.glob('cacm_tok\*.txt'):
    k.append(file.split('\\')[1].split('.txt')[0]);

sorted_list = sorted(k, key=lambda s: s.lower())
#x= k.sort();

docad = 'cacm_tok\\';


#Storing Document length
doc_length= dict()

for f in sorted_list:
    num_lines = sum(1 for line in open(docad+ f  + '.txt'))
    doc_length[f]= num_lines    
    #print num_lines


inv_index=[];

with open('unigram_index.txt') as f2:
    for line in f2:
        x=line.strip().split('->');
        #print x[0]
        if x[0].strip() in query_terms:
            inv_index.append(line.strip());
        #y= ast.literal_eval('[{0}]'.format(x[1]));
        #print y
        #break;
"""      
#with open('inv_index.pickle','wb') as handle:
#    pickle.dump(inv_index,handle);
"""


doc_table=[]

with open('doc_frequency.txt') as f3:
    for line in f3:
        x= line.strip().split(' ');
        if x[0] in query_terms:
            doc_table.append(line.strip());
        #print x[0];        
        #break;
"""

#with open('doc_table.pickle','wb') as handle:
#    pickle.dump(doc_table,handle);

"""


#Inverse Document frequency
for x in doc_table:
    term= x.split(' ')[0];
    df= x.rsplit('->',1)[1].strip()    
    query_terms[term]= 1+ math.log(N*1.0/int(df));

with open('query_terms.pickle','wb') as handle:
    pickle.dump(query_terms,handle);


#Stores the term with the inverted list
term_dict= dict()
term_occ = dict()
for t in inv_index:
    x=t.strip().split('->');
    term= x[0].strip();
    t_list= ast.literal_eval('[{0}]'.format(x[1]));
    #print term;
    #print t_list;
    
    term_dict[term]=t_list;

    for d in t_list:
        if term in term_occ:
            term_occ[term].append(d[0])
        else:
            term_occ[term]= [d[0]]
    
final_p= pandas.DataFrame(index=range(1),\
                          columns=['queryid','Q0','docid','rank','score','sys_name'])
ii=0

#Computation   
for qid,query in queries.iteritems():
    
    docs_score=dict()    
    
    temp_query_terms=[];    
    s=query.split();
    for k in s:    
        if k not in temp_query_terms:
            temp_query_terms.append(k);


    docs_data= dict()
    docs_data = {k:[] for k in sorted_list}
    
    for doc in docs_data:
        sum_query=0
        for t in temp_query_terms:
            if t in term_dict:
                #print t;
                #print t
                if doc in term_occ[t]:
                    #print term_occ[t]
                    for d in term_dict[t]:
                        #print d                        
                        #print d[0]
                        #print doc
                        #print t
                        if d[0]==doc:
                            tf= d[1]*1.0/doc_length[doc]
                            idf= query_terms[t]
                            #print tf
                            #print idf
                            sum_query+= tf*idf;
        #print sum_query
        docs_score[doc]=sum_query;
    scored_list = sorted(docs_score.iteritems(), key=lambda x:-x[1])[:100]  
    #print scored_list      
        #break
    #break
    p= pandas.DataFrame(scored_list, columns=['docid','score'])
    p['queryid']=int(qid)
    p['Q0']='Q0'
    p['rank']= p.index + 1
    p['sys_name']='tfidf'
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
final_p.to_csv('files\\tfidf_low.txt',index=False, sep=' ');

