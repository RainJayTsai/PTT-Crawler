# -*- coding: utf-8 -*-

import sys

sys.path.append('../../src/')

import requests
from bs4 import BeautifulSoup
from pttcrawler import *


soft_res = requests.session()
soft_res = getOver18cookie(soft_res)


index = "1053"
soft_path = "../soft_data/"

import timeit

start = timeit.default_timer()
for i in range(0,100):
    print( "run time: " + str(i) +"\t index number:" + str(index) )

    soft_soup = get_borad_content(soft_res, 'Soft_Job', index)
    index = get_ptt_last_index(soft_soup)

    url_lists, soft_title = article_url_list(soft_soup)
    rslt = crawl(url_lists,soft_title)
    with open( soft_path + str(index+1) + ".json", 'w', encoding='utf-8') as f:
        json.dump(rslt, f, ensure_ascii=False,sort_keys=True)


stop = timeit.default_timer()

print(stop - start )