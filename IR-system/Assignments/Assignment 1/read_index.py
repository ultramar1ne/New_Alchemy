# This file should contain code to receive either a document-id or word or both and output the required metrics. See the assignment description for more detail.
import argparse
import parsing
from nltk.stem import PorterStemmer

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Reading the index")
    parser.add_argument("-d", "--doc", help="the DocName or DOCNO")
    parser.add_argument("-t", "--term", help="the term")
    stemmer = PorterStemmer() # stemmer object for the Porter Stemming algorithm

    # reading and storing the indexies
    termIndex, docIndex, termInfo, termCount = parsing.Tokenization()
    args = parser.parse_args()
    # two arguments
    if args.doc and args.term:
        stemmed_term = stemmer.stem(args.term)

        print("Inverted list for term: ", args.term)
        if stemmed_term in termIndex and args.doc in docIndex:
            termID = termIndex[stemmed_term]
            docID = docIndex[args.doc]

            print("In document: ", args.doc)
            print("TERMID: ", termID)
            print("DOCID: ", docID)

            # look for the term that is matching with the given document
            for doc in termInfo[termID][2]:
                if doc[0] == docID:
                    term_freq = doc[1]
                    term_pos = doc[2]
                    print("Term frequency in document: ", term_freq)
                    print("Positions:", end=' ')
                    print(*term_pos, sep = ', ')
                    break                          
        else:
            print("Error! Either the document or the term is not found.")
    elif args.doc:      # --doc argument
        print("Listing for document: ", args.doc)
        if args.doc in docIndex:
            print("DOCID: ", docIndex[args.doc])
            print("Distinct terms: ", termCount[docIndex[args.doc]]['distinct'])
            print("Total terms: ", termCount[docIndex[args.doc]]['total'])
        else:
            print("Error! Document not found.")
    elif args.term:     # --term argument
        stemmed_term = stemmer.stem(args.term)
        print("Listing for term: ", args.term)
        if stemmed_term in termIndex:
            termID = termIndex[stemmed_term]
            print("TERMID: ", termID)
            print("Number of documents containing term: ", len(termInfo[termID][2]))
            print("Term frequency in corpus: ", termInfo[termIndex[stemmed_term]][1])
        else:
            print("Error! Term not found.")