# -*- coding: utf-8 -*-
"""
Created on Thu Dec 08 18:15:34 2016

Evaluation
@author: Aditya C Awalkar
"""

import pandas


No_Of_Queries=64

#Relevance Calculation
rel_dict ={str((k+1)):[] for k in range(64)};

with open('cacm.rel') as f:
    for line in f:
        entry= line.strip().split()
        qid= entry[0]
        docid = entry[2]
        rel_dict[qid].append(docid);


data = pandas.read_csv('files\\BM25_Query_expansion.txt',sep=' ')
#data = pandas.read_csv('task1_query_result_BM25.csv',sep=',')
#print data

data.columns=['queryid','Q0','docid','rank','score','sys_name']
data= data[['queryid','docid','rank']]
data['Relevance']='N'

#Add Relevance Information
for x in xrange(64):
    qid_data= data[data.queryid==(x+1)]
    #qid_data.reset_index(inplace=True)
    
    for i in qid_data.index:
        if qid_data.loc[i,'docid'] in rel_dict[str(x+1)]:
            #print "rel"
            data.loc[i,'Relevance']='R'
            
    #break
    

data['Precision']=0
data['Recall']=0

#print data


#Precision and Recall


for x in xrange(64):
    qid2_data= data[data.queryid==(x+1)]
    total_rel= len(rel_dict[str(x+1)])    
    rel_count=0
    ret=0
    for i in qid2_data.index:
        ret+=1        
        if qid2_data.loc[i,'Relevance']=='R':
            rel_count+=1;
        if total_rel==0:
            data.loc[i,'Precision']=1.0
            data.loc[i,'Recall']=1.0
        else:
            data.loc[i,'Precision']=1.0* rel_count/ ret
            data.loc[i,'Recall']=1.0* rel_count/ total_rel
    #print x
#print data
    
#data.to_csv('data_chk.txt',sep=',')    



#MAP, MRR

temp_p = 0
temp_rr = 0
for x in xrange(64):
    qid3_data= data[data.queryid==(x+1)]

    #print qid3_data
    #break    
        
    total_rel= len(rel_dict[str(x+1)])
    sum_precision=0
    rr_found=0    
    rr=0
    for i in qid3_data.index:
        
        #if x==4:
            #print i
        if qid3_data.loc[i,'Relevance']=='R':
            
            #Average Precision                
            sum_precision+= data.loc[i,'Precision']
            
            #Reciprocal Rank
            if rr_found==0:
                rr= 1.0/ data.loc[i,'rank']
                rr_found=1;
            
    if total_rel ==0:
        avg_precision= 1.0
    else:
        avg_precision= 1.0 * sum_precision/ total_rel
        #print avg_precision
    temp_p += avg_precision
    temp_rr += rr
mean_avg_p= 1.0 * temp_p/No_Of_Queries
mean_rr = 1.0 * temp_rr/No_Of_Queries

print 'MAP= '+str(mean_avg_p)
print 'MRR= '+ str(mean_rr)


#p@k (k=5 and 20)
pk_list=[]
for x in xrange(64):
    qid_data_pk= data[data.queryid==(x+1)]
    try:
        cond_5= qid_data_pk['rank']==5
        cond_20= qid_data_pk['rank']==20
        r5= qid_data_pk[cond_5].get_value(qid_data_pk[cond_5].index[0],'Precision')
        r20= qid_data_pk[cond_20].get_value(qid_data_pk[cond_20].index[0],'Precision')
    except:
        r5=1
        r20=1
    pk_list.append([str((x+1)), r5, r20])
                    
with open('files\\patk_BM25_Query_expansion.txt','wb') as f:
    for x in pk_list:
        print>>f,''.join(str(y)+' ' for y in x)
        
#Write the file        
data.to_csv('files\\BM25_Query_expansion_eval.txt',sep=' ',index=False)
