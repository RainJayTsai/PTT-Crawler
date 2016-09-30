# -*- coding: utf-8 -*-

import json

import requests
from bs4 import BeautifulSoup


def getOver18cookie(res):
    payload = {
        'from': '/bbs/gossiping/index.html',
        'yes': 'yes'
    }
    res.post('https://www.ptt.cc/ask/over18', data=payload)
    return res
    pass

def get_ptt_last_index(soup):
    indexs = soup.find_all('a', {"class": "btn wide" })
    lastindexstr = indexs[1].get('href')
    board = soup.find("a", "board").contents[1]
    lastindex = int(lastindexstr.lstrip('/bbs/'+board+'/index').rstrip('.html'))
    return lastindex


def crawl(url_list):

    # Create a requests Session
    res = requests.session()

    # get 18+ cookies
    res = getOver18cookie(res)

    rslt = []
    # 送出GET請求到遠端伺服器，伺服器接受請求後回傳<Response [200]>，代表請求成功
    for item in url_list:

        ptt_content = res.get("https://www.ptt.cc/" + item )

        #get board Index html
        soup = BeautifulSoup( ptt_content.text, "html.parser")

        #get article
        rslt.append( parse_article(soup) )




def parse_article(soup):

    #find article all content
    main_content = soup.find("div", id='main-content')

    #find author, title, date
    metas = main_content.select('div.article-metaline')

    author = metas[0].select('span.article-meta-value')[0].string
    title = metas[1].select('span.article-meta-value')[0].string
    date = metas[2].select('span.article-meta-value')[0].string

    # delete information
    [x.extract() for x in metas]
    [x.extract() for x in main_content.select('.article-metaline-right')]
    [x.extract() for x in main_content.select('span.f2')]

    # push info to list and delete it from main_cotnet
    pushlist = [x.extract() for x in main_content.select('div.push')]

    # get article content
    contents = main_content.get_text()

    # push message
    message = []
    for item in pushlist:
        # fix the push is too large bug
        if not item.find('span',"push-tag"):
            continue

        message.append({ "push_tag": item.contents[0].string,
          "user_id" : item.contents[1].string,
          "push_content": item.contents[2].string ,
          "push_ipdatetime":item.contents[3].string
        })


    article = {
        "author" : author,
        "title" : title,
        'date' : date,
        'content' : contents,
        'push' : message,
    }

    return json.dumps(article,indent=4, ensure_ascii=False,sort_keys=True,)


def article_url_list(soup):
    divs = soup.find_all("div",{"class": "r-ent"})

    rslt = []
    for item in divs:
        try:
            rslt.append(item.a.get('href'))
        except:
            #when article is delete do nothing
            pass
    return rslt

def get_borad_content(res, board, index = ""):
    content = res.get('https://www.ptt.cc/bbs/' + board + '/index' + index + '.html')
    soup = BeautifulSoup(content.text, "html.parser")

    return soup

def main():
    from sys import argv
    board = argv[1]
    pages = 1
    print board
    print pages
    if len(argv) == 3:
        try:
            pages = int(argv[2])
        except ValueError:
            print("That's not an number!")
    elif len(argv) == 1:
        raise Exception('argument number error!') # don't, if you catch, likely to hide bugs.


    # Ceata a request seesion
    res = requests.session()

    #fake over 18( get cookie 18 )
    res = getOver18cookie(res)


    #get article url
    soup = get_borad_content(res, board)
    url_lists = article_url_list(soup)


    for i in range(0,pages):
        print crawl(url_lists)
        index = get_ptt_last_index(soup)
        soup = get_borad_content(res,board,index)
        url_lists = article_url_list(soup)


if __name__ == '__main__':
    main()