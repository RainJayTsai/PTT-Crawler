# -*- coding: utf-8 -*-
import argparse
import json
from unittest import TestCase

import requests
import sys
from bs4 import BeautifulSoup

from pttcrawler import parse_article, getOver18cookie, article_url_list, main, get_board_content, crawl


class TestParse_article(TestCase):
    def test_parse_article(self):
        soup = BeautifulSoup(open("./data/tmp.html"), "html.parser")
        z = parse_article(soup)
        j = json.loads(z)
        self.assertEqual(j['author'], u"chucheng (時間太少事情太多)")

    def test_url_list(self):
        import re
        soup = get_board_content(self.res, 'gossiping')
        rslt = article_url_list( soup)
        REGEX = re.compile('/bbs/Gossiping/[A-Za-z0-9\.]*\.html$')
        for item in rslt:
            self.assertTrue(REGEX.search(item))


        pass

    @classmethod
    def setUpClass(self):

        # Ceata a request seesion
        self.res = requests.session()

        #fake over 18( get cookie 18 )
        self.res = getOver18cookie(self.res)


        #get article url
        soup = get_board_content(self.res, 'gossiping')
        self.url_lists = article_url_list(soup)


    def test_crawl(self):
        crawl(["/bbs/Gossiping/M.1472661809.A.BF1.html"])
