import time
import os
import sys
import string
import requests
from bs4 import BeautifulSoup
from priorityQueue import PriorityQueue

class Crawler:
    '''
    A crawler class with methods and attributes to crawl the UCI news articles
    '''
    def __init__(self, seedUrl):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
            'Referer': 'https://news.uci.edu/'
        }
        self.seedUrl = self.readUrl(seedUrl) # starting url for crawler

    # helper
    def readUrl(self, filename):
        '''
        Read the seed url(s) from a file
            filename: name of the file
            return(str): starting(seed) url
        '''
        with open(filename, 'r') as f:
            targetUrl = f.read()
        return targetUrl
    

    def parse_urls(self, url, hasHTML = False):
        '''
        Retrieve the url of articles from the current page
            url: current page that contains a list of articles
            hasHTML: whether to store the html page to file
            return(list) a list of article urls
        '''
        try:
            resp = requests.get(url= url, headers= self.header)
            if resp.status_code != 200:
                raise ValueError('Invalid URL! Please double check seed URL.')
        except Exception as e:
            print(e)
        else:
            soup = BeautifulSoup(resp.text, 'html.parser')
            queue = PriorityQueue()
            # to store the html page
            if hasHTML:
                file_dir = 'data/raw/news_lists/'
                if not os.path.exists(file_dir):
                    os.makedirs(file_dir)
                filename = '%s_%s.html'% (url.split('/')[-3], url.split('/')[-2])
                with open('%s%s' % (file_dir, filename), 'w', encoding='utf-8') as f:
                    f.write(resp.text)

            # retrieve article links
            tags = soup.find_all(class_='row post-item')
            for priority, tag in reversed(list(enumerate(tags))):
                link = tag.a.get('href')
                print('Enqueuing %s..' % link)
                # check for duplicate page
                if not queue.hasDuplicate(link):
                    queue.insert((link, priority))
            
            return queue


    def scrape(self, url, hasHTML = False):
        '''
        Scrape an article's title, sub-title, date and content.
            url: url of the article
            hasHTML: whether to store the html page to file
            return(dict): article data
        '''
        try:
            resp = requests.get(url= url, headers= self.header)
            if resp.status_code != 200:
                raise ValueError('Invalid URL! Please double check seed URL.')
        except Exception as e:
            print(e)
        else:
            soup = BeautifulSoup(resp.text, 'html.parser')
            content = soup.find_all('div', class_ = 'col-md-8 clearfix article article-column-full')
            # content can be in either column wraper
            if content:
                content = content[0]
            else:
                content = soup.find_all('div', class_ = 'col-md-8 clearfix article article-column-wrap')[0]
            article = content.find_all(class_ = 'page-content clearfix')[0].text
            # remove execess empty spaces
            article = article[:article.find('\n\n\n\n')]
            results = {
                'heading' : content.find_all(class_ = 'page-heading')[0].text,
                'sub_heading' : content.find_all(class_ = 'page-subheadline')[0].text,
                'date' : content.find_all(class_ = 'page-date')[0].text.strip(),
                'link' : url,
                'article' : article
            }

            # to store the html page
            if hasHTML:
                file_dir = 'data/raw/news_articles/'
                if not os.path.exists(file_dir):
                    os.makedirs(file_dir)
                filename = results['heading'].translate(str.maketrans('', '', string.punctuation)) # remove any punctuation
                with open('%s%s.html' % (file_dir, filename), 'w', encoding='utf-8') as f:
                    f.write(resp.text)
            return results


    def crawl(self, pages = 71, levels = 2, delay = 1):
        '''
        Automated crawling process that start from the seed url
            pages: number of pages to crawl
            levels: depth to crawl within each page
            delay: time to delay upon each request in seconds
            return: None
        '''
        # https://news.uci.edu/category/campus-news/page/1/
        for page in range(pages):
            url = '{}/page/{}/'.format(self.seedUrl, page + 1)
            article_queue = self.parse_urls(url, hasHTML=True)   # get articles links
            print('--- Currently crawling in page %s/%s ---' % (str(page+1), str(pages)))

            while not article_queue.isEmpty():
                article = article_queue.dequeue()[0]
                data = dict()
                data = self.scrape(article, hasHTML=True)
                print('Dequeued and crawling %s..' % data.get('heading'))

                # store to disk
                file_dir = 'data/articles/'
                if not os.path.exists(file_dir):
                    os.makedirs(file_dir)
                filename = data['heading'].translate(str.maketrans('', '', string.punctuation)) # remove any punctuation
                with open('%s%s' % (file_dir, filename), 'w', encoding='utf-8') as f:
                    f.write('<heading> %s </heading>\n' % data['heading'])
                    f.write('<sub_heading> %s </sub_heading>\n' % (data['sub_heading'] if data['sub_heading'] else 'N/A'))
                    f.write('<date> %s </date>\n' % data['date'])
                    f.write('<link> %s </link>\n' % data['link'])
                    f.write('<article> %s </article>\n' %data['article'])
                time.sleep(delay)
        print('Crawling process has been completed!')


if __name__ == '__main__':
    arguments = len(sys.argv)
    # with pages and levels inputs
    if arguments > 1:
        print(sys.argv[0])
        pages = int(sys.argv[1])
        levels = int(sys.argv[2])
        print('Crawling begins for %d pages with a depth of %d level(s).' % (pages,levels))
        c = Crawler('seed_urls.txt')
        c.crawl(pages, levels)
    else:
        st = time.time()
        c = Crawler('seed_urls.txt')
        c.crawl()
        print("--- Run time: %s seconds ---" % (time.time() - st))
