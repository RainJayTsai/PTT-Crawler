# -*- coding: utf-8 -*-


import requests
from bs4 import  BeautifulSoup

from pttcrawler import getOver18cookie, parse_article

# Ceata a request seesion
res = requests.session()

# fake over 18( get cookie 18 )
res = getOver18cookie(res)

# # get article url
# soup = BeautifulSoup(open("./data/tmp.html", encoding = 'utf8'), "html.parser")
# rslt = parse_article(soup)
#
# print( rslt)
# import json
# import codecs
#
# with codecs.open('./abc.json','w',"utf-8") as abc:
#     x = json.loads(rslt)
#     json.dump(x,abc,ensure_ascii=False)

board = 'soft_job'
url = '/M.1475553514.A.70A.html'
url = '/M.1468489603.A.00A.html'
content = res.get('https://www.ptt.cc/bbs/' + board + url)
soup = BeautifulSoup(content.text, "html.parser")
rslt = parse_article(soup)
print( rslt )