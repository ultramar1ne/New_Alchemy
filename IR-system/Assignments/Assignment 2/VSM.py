import string
import parsing
import sys
import time

def vectorize(src_file):
    result = {}
    queries = []

    with open(src_file, 'r') as f:
        stopwords = open('stopwords.txt', 'r').read()

        # remove punctuation
        for line in f:
            queries.append(line.lower().translate(str.maketrans('','', string.punctuation)))
        
        # break up each query into tokens
        for query in queries:
            tokens = query.split()
            non_stopwords = [t for t in tokens if not t in stopwords]
            # use the query number as the key to query tokens
            result[non_stopwords[0]] = non_stopwords[1:]
    return result


if __name__ == "__main__":
    start_time = time.time()
    arguments = len(sys.argv)

    try:
        query_file = sys.argv[1]
        output_file = sys.argv[2]
    except:
        raise Exception("Please double check the arguments (ex. python ./VSM query_file output_file)")

    result = vectorize(query_file)
    fout = open(output_file, "w")
    #print(result)
    termIndex, docIndex, TokenInfoMap, termCount,DocInfoMap,Index2Dcno=parsing.Tokenization()
    for key,value in result.items():
        rankedlist=parsing.Query(value,termIndex, TokenInfoMap, DocInfoMap,Index2Dcno)
        #print(key,rankedlist[:10])
        i=0
        #<query−number> Q0 <docno> <rank> <score> Exp
        while rankedlist and i<10:
            temp=rankedlist.pop(0)
            text = f'{key} Q0 {temp[0]} {i+1} {temp[1]} Exp\n'
            print(text)
            fout.write(text)
            i+= 1
    fout.close()
    print("--- %s seconds ---" % (time.time() - start_time))