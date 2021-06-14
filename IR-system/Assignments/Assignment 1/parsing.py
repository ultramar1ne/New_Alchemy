import re
import os
import zipfile
import string
import time
import nltk
from nltk.stem import PorterStemmer

def Tokenization():
    fsw=open(r"stopwords.txt",'r')
    stopwords = fsw.read()
    stemmer = PorterStemmer()
    termIndex,docIndex,termInfo=dict(),dict(),dict()
    tokenNum=docNum=0
    termCount=dict()
    # Regular expressions to extract data from the corpus
    doc_regex = re.compile("<DOC>.*?</DOC>", re.DOTALL)
    docno_regex = re.compile("<DOCNO>.*?</DOCNO>")
    text_regex = re.compile("<TEXT>.*?</TEXT>", re.DOTALL)

    with zipfile.ZipFile("ap89_collection_small.zip", 'r') as zip_ref:
        zip_ref.extractall()
    
    # Retrieve the names of all files to be indexed in folder ./ap89_collection_small of the current directory
    for dir_path, dir_names, file_names in os.walk("ap89_collection_small"):
        allfiles = [os.path.join(dir_path, filename).replace("\\", "/") for filename in file_names if (filename != "readme" and filename != ".DS_Store")]
        
    for file in allfiles:
        with open(file, 'r', encoding='ISO-8859-1') as f:
            filedata = f.read()
            result = re.findall(doc_regex, filedata)  # Match the <DOC> tags and fetch documents
            
            for document in result[0:]:
                # Retrieve contents of DOCNO tag
                docno = re.findall(docno_regex, document)[0].replace("<DOCNO>", "").replace("</DOCNO>", "").strip()
                # Retrieve contents of TEXT tag
                text = "".join(re.findall(text_regex, document))\
                        .replace("<TEXT>", "").replace("</TEXT>", "")\
                        .replace("\n", " ")
            
                # step 1 - lower-case words, remove punctuation;create tokens; remove stop-words;stemming
                # step 2 - create tokens 
                text=text.lower()
                without_punctuation="".join([w  if not w in string.punctuation else " " for w in text])
                tokens=without_punctuation.split()
                tokens = [w for w in tokens if not w in stopwords]#use given stopwords
                # stemming(5 points)
                tokens = [stemmer.stem(w) for w in tokens]
                # step 3 - build index
                docIndex[docno]=docNum
                position=0
                for w in tokens:
                    if w not in termIndex:
                        termIndex[w]=tokenNum
                        # include the number of documents that contain the term, number of total occurrences, and 
                        #the posting list (a list of tuples that contain (doc#, frequency in document, [ position1, position2, .....] )         
                        termInfo[tokenNum]=[w,1,[ [docNum,1,[position]] ] ]
                        tokenNum+=1
                    else:
                        temp=termInfo[termIndex[w]].copy()
                        docNumlist=[x[0] for x in temp[-1]]

                        if docNum not in docNumlist:
                            temp[1]+=1
                            temp[-1].append([docNum,1,[position]])
                        else:
                            temp[1]+=1
                            for i in range(len(temp[2])):
                                if temp[2][i][0]==docNum:
                                    temp[2][i][1]+=1
                                    temp[2][i][2].append(position)
                        termInfo[termIndex[w]]=temp
                    position+=1
                termCount[docNum] = {'total' : len(tokens), 'distinct' : len(set(tokens))}
                docNum+=1
    return termIndex, docIndex, termInfo, termCount

            