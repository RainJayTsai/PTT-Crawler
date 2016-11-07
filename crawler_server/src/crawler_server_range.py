# -*- coding: utf-8 -*-

import sys

sys.path.append('../../src/')


import requests
from bs4 import BeautifulSoup
from pttcrawler import *


soft_res = requests.session()
soft_res = getOver18cookie(soft_res)


start = 422
end = 600
soft_path = "../soft_data/"

for index in range(start, end +1 ):
    print( "run time: " + str(index - start) +"\t index number:" + str(index) )

    soft_soup = get_board_content(soft_res, 'Soft_Job', index)
    url_lists, soft_title = article_url_list(soft_soup)
    rslt = crawl(url_lists,soft_title)
    with open( soft_path + str(index) + ".json", 'w', encoding='utf-8') as f:
        json.dump(rslt, f, ensure_ascii=False,sort_keys=True)

