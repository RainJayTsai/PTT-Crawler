# -*- coding: utf-8 -*-
import json
from unittest import TestCase

import requests
from bs4 import BeautifulSoup

from pttcrawler import parse_article, getOver18cookie, article_url_list


class TestParse_article(TestCase):
    def test_parse_article(self):
        soup = BeautifulSoup(open("./data/tmp.html"), "html.parser")
        z = parse_article(soup)
        j = json.loads(z)
        self.assertEqual(j['author'], u"chucheng (時間太少事情太多)")

    def test_url_list(self):
        soup = BeautifulSoup(self.ptt_content.text, "html.parser")
        rslt = article_url_list(soup)
        print rslt
        pass

    @classmethod
    def setUpClass(self):
        # Create a requests Session
        self.res = requests.session()

        # get 18+ cookies
        self.res = getOver18cookie(self.res)

        # 送出GET請求到遠端伺服器，伺服器接受請求後回傳<Response [200]>，代表請求成功
        self.ptt_content = self.res.get("https://www.ptt.cc/bbs/Soft_Job/index.html")
