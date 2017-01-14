# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 23:27:00 2016

Cosine similarity 
@author: Aditya C Awalkar
"""

import pandas
import math
import numpy
import pickle
import glob
import ast

N=3204

def find_magnitude(vec):
    
    #mag= math.sqrt((float(v)*float(v)) for v in vec);
    mag= numpy.linalg.norm(vec);
    return mag;
    
#Query Input
queries=dict()
with open('queries_list.txt') as f:
    i=1    
    for line in f:
        query=line.strip();
        queries[str(i)]= query;
        i+=1;


#Import Document Magnitudes
with open('project_doc_mag.pickle','rb') as handle:
    doc_mag = pickle.load(handle);


#Import idf calculations
with open('query_terms.pickle','rb') as handle:
    query_terms= pickle.load(handle);


k=[];
for file in glob.glob('cacm_tok\*.txt'):
    k.append(file.split('\\')[1].split('.txt')[0]);

sorted_list = sorted(k, key=lambda s: s.lower())



col= query_terms.keys()
    
docs_data = pandas.DataFrame(numpy.nan, index= range(0,N), columns= col ) 
docs_data.insert(0,'docid',sorted_list)
#docs_data.columns= query_terms;


docad = 'cacm_tok\\';

#Storing Document length
doc_length= dict()

for f in sorted_list:
    num_lines = sum(1 for line in open(docad+ f  + '.txt'))
    doc_length[f]= num_lines    




inv_index=[];

with open('unigram_index.txt') as f2:
    for line in f2:
        x=line.strip().split('->');
        #print x[0]
        if x[0].strip() in query_terms:
            inv_index.append(line.strip());




#Term Frequency * Inverse Document Frequency Calculation
for t in inv_index:
    x=t.strip().split('->');
    term= x[0].strip();
    t_list= ast.literal_eval('[{0}]'.format(x[1]));
    #print term;
    #print t_list;
    if term in query_terms:    
    
        for d in t_list:
            tf= d[1]*1.0/doc_length[d[0]]
            idf= query_terms[term];
            docs_data.loc[docs_data.docid == d[0],term]= tf * idf ;

docs_data.fillna(0,inplace=True)


#Cosine Similarity

final_p= pandas.DataFrame(index=range(1),\
                          columns=['queryid','Q0','docid','rank','score','sys_name'])
ii=0



#TF IDF for query
idf_query=1;    
#qid=1;
for qid, q in queries.iteritems():
    #if qid !='1':
        #continue;
    query_tfidf=dict();
    query= q.split(' ');
    
    
    
    for x in query:
        if x not in query_tfidf:
            query_tfidf[x] = 1*1.0/len(query) *idf_query;
        else:
            query_tfidf[x]+=  1*1.0/len(query) * idf_query;
        
    
        
    
    docs_data['cosine_sim']=0;    
    docs_data['rank']=0;    
    for i in xrange(len(docs_data)):   
        
        dot_prod=0;  
        temp=[];
        for y in query_tfidf: 
           if y in docs_data.columns: 
               dot_prod += query_tfidf[y]*docs_data.loc[i,y]; 
           #temp.append(docs_data.loc[i,y]);
        
        mag_doc= find_magnitude(doc_mag[docs_data.loc[i,'docid']]); 
        #print query_tfidf.values();
        mag_query= find_magnitude(query_tfidf.values());   
        cosine_sim = 1.0 * dot_prod / (mag_doc * mag_query);  
        #print "cosine sim= "+ str(cosine_sim);
        docs_data.loc[i,'cosine_sim']=cosine_sim;          
    
    docs_data.fillna(0,inplace=True)
        
    #Ranking top 100
    final = docs_data.sort_values('cosine_sim',ascending=False); 
    #final.insert(); 
    final['rank']=docs_data.index + 1 ;
    final['Q0']='Q0'
    final['system_name']='cosine_similarity'
    final['query_id']= qid;
    final2= final[['query_id','Q0','docid','rank','cosine_sim','system_name']][:100];
    #print final2
    p= pandas.DataFrame(final2, columns=['docid','score'])
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
final_p.to_csv('files\\cosine_sim.txt',index=False, sep=' ');

