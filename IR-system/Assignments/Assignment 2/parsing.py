import re
import os
import zipfile
import string
from nltk.stem import PorterStemmer
class TokenInfo(object):
    def __init__(self,word:str, times:int,inDocMap:dict,inDocList:list ):
        self.word = word 
        self.times = times
        self.inDocMap = inDocMap
        self.inDocList= inDocList
#      inDocMap( Key: docNum; Value: (times,[position]) )

 
# key DocNum, Value: DocTokens
def Tokenization():
    fsw=open(r"stopwords.txt",'r')
    stopwords = fsw.read()
    stemmer = PorterStemmer()
    termIndex,docIndex=dict(),dict()
    tokenNum=docNum=0
    termCount=dict()
    Index2Dcno=dict()
#######Newly added Data Struct:
    TokenInfoMap=dict()
# key: TokenID; Value : TokenInfo (class written above)
# To Do: class DocInfo    
    DocInfoMap=dict()   
    # Regular expressions to extract data from the corpus
    doc_regex = re.compile("<DOC>.*?</DOC>", re.DOTALL)
    docno_regex = re.compile("<DOCNO>.*?</DOCNO>")
    text_regex = re.compile("<TEXT>.*?</TEXT>", re.DOTALL)

    # with zipfile.ZipFile("ap89_collection_small.zip", 'r') as zip_ref:
    #     zip_ref.extractall()
    
    # Retrieve the names of all files to be indexed in folder ./ap89_collection_small of the current directory
    for dir_path, dir_names, file_names in os.walk("ap89_collection_small"):
        allfiles = [os.path.join(dir_path, filename).replace("\\", "/") for filename in file_names if (filename != "readme" and filename != ".DS_Store")]
        
    for file in allfiles:
        with open(file, 'r', encoding='ISO-8859-1') as f:
            filedata = f.read()
            result = re.findall(doc_regex, filedata)  # Match the <DOC> tags and fetch documents
            
            # TO del:!!!!
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
                Index2Dcno[docNum]=docno
                position=0
                for w in tokens:
                    if w not in termIndex:
                        termIndex[w]=tokenNum
                        # include the number of documents that contain the term, number of total occurrences, and 
                        #the posting list (a list of tuples that contain (doc#, frequency in document, [ position1, position2, .....] )         
                        #termInfo[tokenNum]=[w,1,[ [docNum,1,[position]] ] ]
                        TokenInfoMap[tokenNum]=TokenInfo(w,1,{docNum: [1,[position]]},[docNum])
                        tokenNum+=1
                    else:
                        tempTokenInfo=TokenInfoMap[termIndex[w]]
                        if docNum not in tempTokenInfo.inDocList :
                            tempTokenInfo.times+=1
                            tempTokenInfo.inDocList.append(docNum)
                            tempTokenInfo.inDocMap[docNum]=[1,[position]]
                        else:
                            tempTokenInfo.times+=1
                            tempDocMapItem=tempTokenInfo.inDocMap[docNum]
                            tempDocMapItem[0]+=1
                            tempDocMapItem[1].append(position)
                            tempTokenInfo.inDocMap[docNum]=tempDocMapItem
                        TokenInfoMap[tokenNum]=tempTokenInfo
                    position+=1
                termCount[docNum] = {'total' : len(tokens), 'distinct' : len(set(tokens))}
                DocInfoMap[docNum]=tokens
                
                # end of a doc                
                docNum+=1
    return termIndex, docIndex, TokenInfoMap, termCount,DocInfoMap,Index2Dcno

#print(TokenInfoMap[2].inDocList)
#print(TokenInfoMap[2].inDocMap[0])

def Tokenize4Query(text : str):
    text=text.lower()
    fsw=open(r"stopwords.txt",'r')
    stopwords = fsw.read()
    stemmer = PorterStemmer()
    without_punctuation="".join([w  if not w in string.punctuation else " " for w in text])
    tokens=without_punctuation.split()
    tokens = [w for w in tokens if not w in stopwords]#use given stopwords
    tokens = [stemmer.stem(w) for w in tokens]
    return tokens

def CosSim(queryTokens :list , docNum:int,DocInfoMap):
    docTokens=DocInfoMap[docNum]
    allTokens=docTokens+queryTokens
    allTokens=list(set(allTokens))
    docBinary=[]
    docLength=0
    queryBinary=[]
    queryLength=0
    for token in allTokens:
        if token in docTokens:
            docBinary.append(1)
            docLength+=1
        else:
            docBinary.append(0)
        if token in queryTokens:
            queryBinary.append(1)
            queryLength+=1
        else:
            queryBinary.append(0)
    result=(sum(map(lambda e,f:e*f, queryBinary,docBinary))) / ((docLength*queryLength)**0.5)
    return result


def findRelatedDocNum(queryTokens,termIndex,TokenInfoMap):
    relatedDocList=[]
    for token in queryTokens:
        if token not in termIndex:
            continue
        else:
            ToAdd=TokenInfoMap[termIndex[token]].inDocList
        for docNum in ToAdd:
            if docNum not in relatedDocList:
                relatedDocList.append(docNum)
    return relatedDocList
            
def Query(queryTokens,termIndex, TokenInfoMap, DocInfoMap,Index2Dcno):
    #queryTokens=Tokenize4Query(query)
    relatedDocList=findRelatedDocNum(queryTokens,termIndex,TokenInfoMap)
    toRanklist=[]
    for docNum in relatedDocList:
        #print(docNum)
        toRanklist.append( (Index2Dcno[docNum],CosSim(queryTokens,docNum,DocInfoMap)) )
    toRanklist.sort(key=takeSecond,reverse=True)
    return toRanklist
#termIndex, docIndex, TokenInfoMap, termCount,DocInfoMap=Tokenization()
#queryStr="Document will identify acquisition by the U.S. Army of specified advanced weapons systems"
def takeSecond(elem):
    return elem[1]
#print( Query(queryStr,termIndex, TokenInfoMap, DocInfoMap))
    