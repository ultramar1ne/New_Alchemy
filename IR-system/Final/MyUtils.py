import nltk
import MyAbstract
nltk.download('punkt')
# Use nltk.tokenize here is not a waste
# In fact it can not only improve the accuracy and avoid many corner case,
# but also protect from some "injection attacks"

def generteDsl(q):
    tokens=nltk.word_tokenize(q)
    if not tokens:
        dsl_1={
        "query": {
        "match_all": {}
         }
    }

    elif len(tokens)==1:
        dsl_1 = {
    "query": {
        "function_score": {
            "query": {
                "fuzzy": {
                    "text": {
                        "value": tokens[0],
                        "fuzziness": 1
                    }
                }
            },
            "field_value_factor": {
                "field": "timeScore",
                "modifier": "log1p",
                "factor": 0.1,
                "missing": 1
            },
            "boost_mode": "sum"
        }
    },

    "rescore": {
        "window_size": 50,
        "query": {
            "rescore_query": {
                "match": {
                    "important": q
                }
            },
            "query_weight": 1,
            "rescore_query_weight": 0.5
        }
    }
}
    else:
        dsl_1={
            "query": {
                "multi_match": {
                "query": " ".join(tokens),
                "fields":["text","important"],
                "slop": len(tokens)-1
                }
            }
        }
    return dsl_1

def printResult(response):
    for i in range(len(response["hits"]["hits"])):
        if i > 10:
            break
        temp = response["hits"]["hits"][i]
        print("Number:", i+1 , "Score:  %.3f"%temp["_score"], "  Title: ", temp['_source']['news_title'].replace("â","").replace("",""))
        if temp['_source']["text"]:
            print ("2-Sentences Abstract of the News:  ", MyAbstract.generateSummary(temp['_source']["text"],2))
            print(" ")

