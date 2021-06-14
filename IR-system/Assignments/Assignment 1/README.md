# CS172 - Assignment 1 (Tokenization)

## Team member 1 - Yanjun Zhu
## Team member 2 - Qun Lou

###### Provide a short explanation of your design
Create token
- In the token processing, we used the python built-in methods to do the lower case and to remove puncution. To remove stop words, we read in the stopwords as a list and filter it from our token list.
- We used the PorterStemmer algorithm from the NLTK library to do the stemming.

Build index
- We use dictionary to build the `termIds`, `docIds`and `termInfo`.
  - Both `termIds` and  `docIds` are single value dict that maps an unique id to each term and DOCNO respectively.
  - `termInfo` is in the structure as `termid : ['token', total_occur, [[doc_id, freq_in_doc, [positions]]]`

Read index
 - We implemented the command line interface using the argparse library and include the `--doc` and `--term` as optional arguments.

Storing indices on disk (extra credict)
 - we create the `external_storing.py` to generate data files to meet the required formats.

###### Language used, how to run your code, if you attempted the extra credit (stemming), etc. 
- The language we used is python.
- To run the program: `pythoon read_index.py --doc DOC --term TERM`
- Extra credit attempted: 
  - Stemming
  - Creating files (on disk)
   - The following files are generated using  `python external_storing.py`:
    -  docids.txt
    -  term_index.txt
    -  term_info.txt
    -  termids.txt 
