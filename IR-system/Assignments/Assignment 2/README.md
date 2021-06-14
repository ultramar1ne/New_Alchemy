# CS172 - Assignment 2 (Retrieval)

## Team member 1 - Yanjun Zhu
## Team member 2 - Qun Lou

###### Provide a short explanation of your design

## Steps:
## 1. Build Multiple (inverted) Maps as HW1
We also re-wrote some important data structures within *class* to improve the efficiency for both coding and program running.
### 1.1 Vectorize
- convert the queries from `query_list.txt` into a token vector.

## 2. Query
### 2.0 Vectorize
We tokenize the input query, delete its QNO, and so on.

### 2.1 Find Related Docs
To reduece time complexity, we won't just burte-force every documents. In deed, we will first search which docs are needed, which is O(n) time-consuming where n is only the length of a query! This step can save 70% time as we tested.

### 2.2 Calculate Cosine-Similarity
For one of the "Related Docs" and the query
1) build the one-hot-vector for them（We think "binary weigh" is as the same as one-hot-vector
2) calculate the Cosine-Similarity


###### Language used, how to run your code, if you attempted the extra credit (stemming), etc. 
- The language we used is python.
- To run the program: `python VSM.py < query−file > < name−of−results−file >` `ex. python VSM.py query_list.txt output.txt`
- The `output.txt` has the sample output to the top 10 rankings of each query of the given query_list.txt.

###### Extra credit
We did not attempt.
