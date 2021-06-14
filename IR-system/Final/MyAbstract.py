import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx

stopwords= set(stopwords.words('english'))
def sentenceCosSim(sent1, sent2, stopwords=[]):   # 1-CosDistance(v1,v2)
    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]
    all_words = list(set(sent1 + sent2))
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
    # build the one-hot vector for the 2 sentences
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] = 1
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] = 1
    return 1 - cosine_distance(vector1, vector2)

def generateSimilarityMatrix(sentences, stop_words=None):
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
    for s1 in range(len(sentences)):
        for s2 in range(len(sentences)):
            similarity_matrix[s1][s2] = sentenceCosSim(sentences[s1], sentences[s2], stop_words)
    return similarity_matrix

def generateSummary(text, top_n = 4):
    summarize_text = []
    sentences = nltk.sent_tokenize(text) #Use NLTK to divide sentece
    martix = generateSimilarityMatrix(sentences,stopwords)
    graph = nx.from_numpy_array(martix)
    scores = nx.pagerank(graph)
    ranked_sentence = sorted(((scores[i], s) for i,s in enumerate(sentences)), reverse= True)
    for i in range(top_n):
        try:
            summarize_text.append("".join(ranked_sentence[i][1]))
        except IndexError as es1:
            return ".".join(summarize_text).replace("â","").replace("","")
    return ".".join(summarize_text).replace("â","").replace("","")