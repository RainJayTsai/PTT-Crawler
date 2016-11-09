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


def crawl(url_list,title=None):

    # Create a requests Session
    res = requests.session()

    # get 18+ cookies
    res = getOver18cookie(res)
    rslt = []
    # 送出GET請求到遠端伺服器，伺服器接受請求後回傳<Response [200]>，代表請求成功
    for i,item in enumerate(url_list):
        # print(item)
        ptt_content = res.get("https://www.ptt.cc/" + item)

        # get article error
        if ptt_content.status_code != 200:
            continue

        #get atricle
        soup = BeautifulSoup( ptt_content.text, "html.parser")

        #get article of json
        if title is None:
            x = parse_article(soup)
        else:
            x = parse_article(soup,title[i])
        if( x is not None):
            x['url'] = item
            rslt.append( x )

    return rslt



def parse_article(soup, titlex=None):
    try:
        #find article all content
        main_content = soup.find("div", id='main-content')

        #find author, title, date
        metas = main_content.select('div.article-metaline')
        author = ''
        date = ''
        if titlex is not None:
            title = titlex
        else:
            title = ''

        if metas and len(metas) == 3:
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
        cf_email_decode(main_content)
        contents = main_content.get_text()

        if contents == "":
            return None

        # push message
        message = []
        for item in pushlist:
            # fix the push is too large bug
            if not item.find('span',"push-tag"):
                continue

            message.append({ "push_tag": item.contents[0].string,
              "push_id" : item.contents[1].string,
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

        # return json.dumps(article,indent=4, ensure_ascii=False,sort_keys=True,)
        return article
    except:
        print("Error in Title: ",titlex)

def article_url_list(soup):
    divs = soup.find_all("div",{"class": "r-ent"})

    rslt_url = []
    rslt_title = []
    for item in divs:
        try:
            rslt_url.append(item.a.get('href'))
            rslt_title.append(item.a.string)
        except:
            #when article is delete do nothing
            pass
    return rslt_url, rslt_title

def get_board_content(res, board, index =""):
    content = res.get('https://www.ptt.cc/bbs/' + board + '/index' + str(index) + '.html')
    soup = BeautifulSoup(content.text, "html.parser")

    return soup

def main():
    from sys import argv
    board = argv[1]
    pages = 1

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
    soup = get_board_content(res, board)
    url_lists = article_url_list(soup)


    for i in range(0,pages):
        print(crawl(url_lists) )
        index = get_ptt_last_index(soup)
        soup = get_board_content(res, board, index)
        url_lists = article_url_list(soup)



def cf_email_decode(soup):

    def decodex(e):
        de = ""
        k = int(e[:2], 16)

        for i in range(2, len(e)-1, 2):
            de += chr(int(e[i:i+2], 16)^k)
        return de


    for item in soup.select('a.__cf_email__'):
            cfemail = item.get('data-cfemail')
            item.replace_with(decodex(cfemail))

    [ x.extract() for x in soup.select('script[data-cfhash]') ]


def pttCrawler(index="", board="", pages=1, url=None):
    if url:
        url = url[url.lower().find('/bbs'):]
        return crawl([url])
    else:
        res = requests.session()
        res = getOver18cookie(res)

        rslt = []
        for i in range(0,pages):
            soup = get_board_content(res, board, index)
            url_lists, soft_title = article_url_list(soup)
            rslt.extend(crawl(url_lists,soft_title))
            index = index - 1
        return rslt

if __name__ == '__main__':
    main()