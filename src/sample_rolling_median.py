
# coding: utf-8

# In[6]:

import os.path
import json
import collections
import datetime
from statistics import median # this is a standard library in python 3.5

# set input , output path for any operating system
fpath = os.path.join("venmo_input", "venmo-trans.txt")
opath = os.path.join("venmo_output", "output.txt")

json_data=open(fpath).readline()
data = json.loads(json_data)

maxtimestamp=datetime.datetime(1, 1, 1, 1, 1, 1)
datehv1=data['created_time'].replace('T', ' ')
datahv2=datehv1.replace('Z', '')
transdatetime=datetime.datetime.strptime(datahv2, "%Y-%m-%d %H:%M:%S")

# TranLast60 is a list of lists which keep all transactions in the last 60 seconds
TranLast60 =[]
outfile=open(opath,'w')
outfile.close()

meddegreetime=[] # keep median degree of vertices over time for debugging purposes, could be removed for very large data
outfile=open(opath,'w')
maxtimestamp=datetime.datetime(1, 1, 1, 1, 1, 1) # initialized with an early time in the past
for line in open(fpath):
    data = json.loads(line)
    datehv1=data['created_time'].replace('T', ' ')
    datahv2=datehv1.replace('Z', '')
    transdatetime=datetime.datetime.strptime(datahv2, "%Y-%m-%d %H:%M:%S")
    if data['actor']!='' and data['target']!='' and data['created_time']!='':
        TranLast60.append([transdatetime,data['actor'],data['target']])
        if transdatetime>maxtimestamp:
            maxtimestamp=transdatetime
        
        # This part filter the transactions according to the 60 seconds timeframe
        FilteredTranLast60=[]
        for recordind, recordvalue in enumerate(TranLast60):
               if not (TranLast60[recordind][0]-maxtimestamp)> datetime.timedelta(seconds=60) and not (maxtimestamp-TranLast60[recordind][0])> datetime.timedelta(seconds=60):
                    FilteredTranLast60.append(TranLast60[recordind])
        TranLast60=FilteredTranLast60
        # End of filtering part

        # this part build the graph from last 60 transaction record, each record is a dictionary whose key is the name of one person
        graph=collections.defaultdict(list)
        for recordind, recordvalue in enumerate(TranLast60):
            graph[TranLast60[recordind][1]].append(TranLast60[recordind][2])
            graph[TranLast60[recordind][2]].append(TranLast60[recordind][1])
        # end of graph

        # Create a list of degrees for all vertices at the current point
        degree={}
        for key in graph:
            if len(list(set(graph[key])))>0:
                degree[key]=len(list(set(graph[key])))
        # end of list of degrees 

        # calculating median and write it to the output
        currentmeddegree=median(sorted(degree.values()))  
        outfile.write(str(format(currentmeddegree,'.2f'))+'\n') # write the float median with two decimal digits to be compatible with the provided test vector
        meddegreetime.append(currentmeddegree) # could be removed if data gets very large
   
    else: # error handling if an empty record received
        print('one transaction at ',data['created_time'],' ignored due to corrupted data')

outfile.close()    


# In[ ]:



