# -*- coding: utf-8 -*-
"""
Created on Tue Dec 05 16:13:02 2016

Maginitude of the Documents
@author: Aditya C Awalkar
"""

import math;
import ast;
import glob;
import pickle;
import numpy;


def find_magnitude(vec):
    
    #mag= math.sqrt((float(v)*float(v)) for v in vec);
    mag= numpy.linalg.norm(vec);
    return mag;


N=3204;


k=[];
for file in glob.glob('cacm_tok\*.txt'):
    k.append(file.strip().split('.txt')[0].split('\\')[1]);

sorted_list = sorted(k, key=lambda s: s.lower())
#x= k.sort();

docad = 'cacm_tok\\';


#Storing Document length
doc_length= dict()

for f in sorted_list:
    num_lines = sum(1 for line in open(docad+ f  + '.txt'))
    doc_length[f]= num_lines    
    #print num_lines


#Document DIct for tf*idf
doc_tfidf= dict();
doc_tfidf ={k:[] for k in doc_length} 


inv_index= [];

with open('unigram_index.txt') as f2:
    for line in f2:
        x=line.strip().split('->');
        #print x[0]
        inv_index.append(line.strip());
        #y= ast.literal_eval('[{0}]'.format(x[1]));
        #print y
        #break;


doc_table= [];
idf_terms= dict();
with open('doc_frequency.txt') as f3:
    for line in f3:
        x= line.strip().split(' ');
        doc_table.append(line.strip());
        #print x[0];        
        #break;


#Inverse Document frequency
for x in doc_table:
    term= x.split(' ')[0];
    df= x.rsplit('->',1)[1].strip()    
    idf_terms[term]= 1+ math.log(N*1.0/int(df));


#Term Frequency * Inverse Document Frequency Calculation
for t in inv_index:
    x=t.strip().split('->');
    term= x[0].strip();
    t_list= ast.literal_eval('[{0}]'.format(x[1]));
    #print term;
    #print t_list;
    
    for d in t_list:
        tf= d[1]*1.0/doc_length[d[0]]
        idf= idf_terms[term];
        doc_tfidf[d[0]].append(tf*idf);
        #docs_data.loc[d[0]-1,term]= tf * idf ;


#Calculate the magnitude
doc_mag=dict()

for doc,value in doc_tfidf.iteritems():
    doc_mag[doc]= find_magnitude(value);
    #print doc
    #print value;
    #break;
    
with open('project_doc_mag.pickle','wb') as handle:
   pickle.dump(doc_mag,handle);

