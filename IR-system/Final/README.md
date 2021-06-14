# ToDo:
1. 接口
2. .sh脚本 安装依赖？
3. 网页

功能上应该没问题了，我测的时候有时候会读取超时我怀疑是国内网络原因

# Information Retrieval System for UCI News Articles
 This is an information retrieval system which involved with techniques for indexing and searching.
 
## Collaboration Details:
(Description of contribution of each team member.)
 - Yanjun Zhu
 - Qun Lou

## Project
### Part 1 - Crawler
Overview of system, including (but not limited to)

- (a) Architecture
- (b) The Crawling or data collection strategy (do you handle duplicate URLs, is your crawler parallel, etc.)
- (c) Data Structures employed

Limitations (if any) of the system.

Instruction on how to deploy the crawler. Ideally, you should include a crawler.bat (Windows) or crawler.sh (Unix/Linux) executable file that takes as input all necessary parameters. Example instructions for Web-based assignment: [user@server]./crawler.sh < seed − Fileseed.txt > < num − pages : 10000 > < hops − away : 6 > <output−dir >

### Part 2 - Indexer
Instructions on how to deploy the system. Ideally, you should include an indexer.bat (Windows) or indexer.sh (Unix/Linux) executable file that takes as input all necessary parameters .  Example: [user@server] ./indexer.sh < output − dir >
#### Take these Factors into Considerations:
1. *Time* is an important metric. Because we focused on the "news" webpages, the more ***recent*** the news was posted, the more important we think it is.
2. *Titles* and *SubTitles* should be calculated with regard to final scores.
3. We tokenize the input query, so it will be more accurate and avoid some injecting attacks.
4. We allow *fuzzyness* to some extent.
5. Robustness.  We figured out some errors ocassionaly happened in our program.

### Part 3 - Extension
Detailed description of your ‘extension’ and motivation or benefit of the implemented feature or extension. Include screen shots of your system in action.
####  Abstract Generation
Build one-hot vectors from each two sentences and calculte the cos-similarity like hw2. And we just use nltk built-in functions this time.
Build the score matrix and graph, pick the top 2 sentences to make up the *Abstract* .

## Setup
...

## Usage
...
