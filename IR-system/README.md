# Information Retrieval System for UCI News Articles
 This is an information retrieval system which involved with techniques for indexing and searching.
 
## Collaboration Details:
(Description of contribution of each team member.)
 - Yanjun Zhu (Crawler and parsing the data for ElasticSearch)
 - Qun Lou (ElasticSearch and Snippet results)

## Project
### Part 1 - Crawler
Overview of system, including (but not limited to)

The website we are crawling is the [UCI news](https://news.uci.edu/category/campus-news)
- (a) We first start from the seed urls in `seed_urls.txt`.
- (b) The Crawling or data collection strategy (do you handle duplicate URLs, is your crawler parallel, etc.)
  - We implemented the priority queue to queue up URLs that is found within each page of the list of articles.
  - We enqueue new appearing urls while we crawl, in the meantime we also handle duplicate URL by checking if the url is found within the queue.
  - The crawling process finishes when it reaches the user specific page and the queue is empty.
  - The crawled data are stored in the `data` folder where it has the `raw` which contains the htmls and `articles` are the parsed articles.
- (c) Data Structures employed:
  - Prioirty queue.
  - Dictionary to map the results.

Limitations of the system:
- Since the crawler is not running in multi-threaded we are enforcing a delay of 1 second upon each requests.

To deploy the crawler:
Please refer to the `usage` section below.

### Part 2 - Indexer

There are 3 helper `.py` files to generate the necessary parameters for the ElasticSearch in `es.py`:
- `readfile.py` iterates through the `articles` folder to index the title, subtitle, date, link and text of each article.
- `MyAbstract.py` contains methods to generate the snippet result(part 3- extension) based on the result.
- `MyUtils.py` generate DSL of the input query and build a DSL map according to the Query's token length

The `es.py` utilize all these helper classes to perform ElasticSearch based on the query keywords.

#### Take these Factors into Considerations for ElasticSearch:
1. *Time* is an important metric. Because we focused on the "news" webpages, the more ***recent*** the news was posted, the more important we think it is.
2. *Titles* and *SubTitles* should be calculated with regard to final scores.
3. We tokenize the input query, so it will be more accurate and avoid some injecting attacks.
4. We allow *fuzzyness* to some extent.
5. Robustness.  We figured out some errors ocassionaly happened in our program.

### Part 3 - Extension
Snipet Results
 - Display a snipet result using the sent_tokenize function from `nltk`and to generate a scoring graph with the `networkx` library.
 - Build one-hot vectors from each two sentences and calculte the cos-similarity similar in assignment 2. And we just use nltk built-in functions this time.
 - Build the score matrix and graph, pick the top 2 sentences to make up the *Abstract* of the article.

## Result
Sample output of the ElasticSearch of the word "science":
![output](https://github.com/ayjzhu/IR-system/blob/main/doc/sample_output.jpg)

## Setup
### Required libraries:
- requests
- bs4 (Beautifulsoup)
- elasticsearch
- nltk
- networkx

## Usage
### To run the crawler:
`python crawler.py <pages> <levels>`
 - pages: number of pages to crawl (default 71)
 - levels: the level of depth to crawl within each page (default 2)
 
`Ex. python crawler.py 2 2` or `python crawler.py` to crawl all pages with a depth of 2.
 
 ### To run the ElasticSearch (IR system):
 1. `python es.py`
 2. Input search keywords.
 3. The program outputs the top 10 results base on the query in the console.
