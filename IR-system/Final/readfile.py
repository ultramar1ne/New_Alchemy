import os
import re
heading_regex = re.compile("<heading>.*?</heading>", re.DOTALL)
subHeading_regex = re.compile("<sub_heading>.*?</sub_heading>", re.DOTALL)
date_regex = re.compile("<date>.*?</date>")
text_regex = re.compile("<article>.*?</article>", re.DOTALL)
def walkFile(file):
    articles=[]
    for root, dirs, files in os.walk(file):
        for file in files:
            with open(os.path.join(root, file), 'r', encoding='ISO-8859-1') as f:
                filedata = f.read()
                heading=re.findall(heading_regex, filedata)[0].replace("<heading>", "").replace("</heading>", "").strip()
                subHeading=re.findall(subHeading_regex,filedata)[0].replace("</sub_heading>", "").replace("<sub_heading>", "").strip()
                try:
                    year=re.findall(date_regex,filedata)[0].replace("</date>", "").replace("<date>", "").strip()
                except IndexError as es1:
                    year="2016 "
                text=re.findall(text_regex,filedata)[0].replace("</article>", "").replace("<article>", "").strip()
                try:
                    yearScore= (int(year[-5:])-2000)/10
                except IndexError as es1:
                    yearScore=1
                art= {
                    "news_title": heading,
                    "news_sub_title" : subHeading,
                    "important":heading+subHeading,
                    "text": text,
                    'timeScore':yearScore
                    }
                articles.append(art)
    return articles
