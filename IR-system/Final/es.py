# -*- coding: utf-8 -*-
""" https://colab.research.google.com/drive/13VKBkJxn-hA27275j-WNFFnuJ1O0gJtP """
import readfile,MyUtils
from elasticsearch import Elasticsearch,RequestError
import time
# QunLou's Cloud Pass:
elastic_pass = "3plH38ggNcmF0AjbwSkbZW4G"
elastic_endpoint = "i-o-optimized-deployment-352d73.es.us-west1.gcp.cloud.es.io:9243"
connection_string = "https://elastic:" + elastic_pass + "@" + elastic_endpoint
print(connection_string)

indexName = "cs172" + "2502"#str(time.time())[-4:] # avoid repeated indexName

esConn = Elasticsearch(connection_string)
creatflag = 0
try:
    response = esConn.indices.create(index=indexName)  # create index
except RequestError as es1:
  print('Index already exists!!')
  creatflag=1
# 1. OpenFile->ES
if creatflag==0:
    start = time.time()
    docs = readfile.walkFile("data/articles")
    docID = 0
    for doc in docs:
        response = esConn.index(index=indexName, id=docID, body=doc)
        if docID%100==0:
            print (response)  # result status
            end = time.time()
            running_time = end - start
            print('time cost : %.5f sec' % running_time)
        docID += 1

# Take into consideration:
# 0. fuzzy
# 1. Time's Weights
# 2. Title's Weights.    2.1 Multi Querries
# 3. install ES locally or just use Cloud?   3.1 Concurunt I/O? ; Use Redis?
# 4. UCI-> UC Irvine?

querys = ["crime","virtual reality","riverside","sports champion campus female"]

for q in querys:
    print('~~Query:',q,'~~~  Results:')
    response = esConn.search(index=indexName, body=MyUtils.generteDsl(q))
# print (response) #result status
    MyUtils.printResult(response)

# To Do:
# 3. Output->Website front end