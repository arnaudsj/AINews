# AINewsFinder 
# Copyright (C) 2010 
# Author:   Liang Dong <ldong@clemson.edu>
# URL: <http://bioinformatics.clemson.edu/ldong>
# $Id$

"""
With funds allocated by the Executive Committee, we have hired a summer intern
to bring AI in the News back online as a twice-monthly service. Liang Dong,
a CS graduate student from Clemson, is automating the service, under the
supervision of Bruce Buchanan and Reid Smith, with an AI program, called
NewsFinder. It first pulls in RSS feeds from Google News and other reliable
sources and filters out blogs, press releases, and advertisements. A support
vector machine has been trained with manually scored stories from the web to
classify each story as "not relevant to AI" (0), or "very interesting" (+5),
"somewhat interesting" (+3), or "mildly interesting" (+1).

We augment the SVM's scores with a measure of interest (frequency * inverse
doc frequency) of selected terms and additional heuristics (using multi-word
phrases) that indicate higher or lower interest. The sources of the articles
will also be considered, since appearance of a story in a major news publication
like the NY Times makes it more likely to be asked about.

"""

import sys
import os
import getopt
import locale

from AINewsConfig import config, paths
from AINewsCrawler import AINewsCrawler
from AINewsPublisher import AINewsPublisher

def usage():
    """
    Print out the command-line usage of AINews.py.
    """
    usage = """                AINews Finder 
    USAGE:
        python AINews.py COMMAND [OPTION]
    COMMAND:
        (1) crawl:
            crawl latest news from outside web.

        (2) train:
            train news classifiers based on human rates.
            
        (3) publish:
            publish news from output files to Pmwiki site and send emails.
            It is weekly publish to the public.
            
        View Latest news at:
        http://www.aaai.org/AITopics/AINews
            
        """

    print usage
    
    
def crawl(opts):
    crawler = AINewsCrawler()
    crawler.crawl()

def train():
    svm = AINewsSVM()
    svm.collect_feedback()
    svm.load_news_words()
    svm.train_all()
    svm.train_isrelated()

def publish():
    publisher = AINewsPublisher()
    publisher.filter_and_process()
    publisher.generate_standard_output()
    publisher.generate_email_output()
    publisher.generate_pmwiki_output()
    publisher.publish_email()
    publisher.publish_pmwiki()
    publisher.update_rss()

def main():
    """
    Main function of AINews.py
    """
    # Set en_US, UTF8
    locale.setlocale(locale.LC_ALL,'en_US.UTF-8')

    commands_list = ("train", "crawl", "publish", "help")
    try:
        if len(sys.argv) < 2 or sys.argv[1] not in commands_list:
            usage()
            sys.exit()
        command = sys.argv[1]
        opts, args = getopt.getopt(sys.argv[2:], 'rf:u:', ['url=', 'file=', 'rss'])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    if command == "train":
        train()

    elif command == "crawl":
        crawl(opts)

    elif command == "publish":
        publish()

if __name__ == "__main__":
    main()

