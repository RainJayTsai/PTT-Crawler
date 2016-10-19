# -*- coding: utf-8 -*-
import csv
import json
import jieba
import jieba.analyse
from sklearn.cluster import KMeans
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.svm import OneClassSVM

start = 300
end = 600
path = "../soft_data/"

re_word = re.compile("\[[\u4e00-\u9fa5]*\]\s")

def saveTitleOneFile():

    title = []

    for index in range(start,end + 1 ):
        with open(path + str(index) + ".json", 'r',encoding='utf8') as f:
            tmp = json.load(f)
        for item in tmp:
            if item['title'] is not  None:
                title.append(item['title'])

    with open("title300_600.json", 'w', encoding='utf8') as f:
        json.dump(title,f,ensure_ascii=False,sort_keys=True)


def getFeature():
    with open( "title300_600.json", 'r', encoding='utf8') as f:
        titles = json.load(f)

    jieba.load_userdict("../data/userdict.txt")

    for i,item in enumerate(titles):
        if item.strip().find("Re:") != -1:
            titles.remove(item)
        else:
            tmp = re_word.split( item.strip().strip("Fw: ") )
            if len( tmp ) == 2:
                titles[i] = tmp[1]

    tmp = []
    for item in titles:
        tmp.append(" ".join( jieba.cut(item)))

    titles = tmp
    tfidf = TfidfVectorizer()
    X = tfidf.fit_transform(titles)
    print(tfidf.get_feature_names())

def titletoCSV():
    with open( "title300_600.json", 'r', encoding='utf8') as f:
        titles = json.load(f)

    keys = [ 'Python', 'Java', '研替', '研發替', 'htc', '華碩', '台積電', '聯發科', 'mtk', 'qnap','offer',
             '群暉', '和碩','華電信', '中鋼', '亞太', '京群', '人資','仁寶', '傑聯特','偉康', '偉嘉','傳媒', '優必達', '優碩','優酷',
             '元大', '兆豐','光寶', '冠信', '凌網', '凌群', '凱信', '凱衛', '凱鈿', '力鯨','創見','勝華','勤崴', '勤業', '南港',
             '台揚','台達電', '啟翔','龍網', '龍騰', '鼎新','鴻佰', '鴻凱', '鴻揚', '鴻海','面試','願境','kkbox','資拓',
             '感謝函']
    # classs = ['請益', '推坑', '討論', '心得']
    classs = [ '徵文', '板務', '公告', '問卷', '開獎']

    with open("title_c2.csv",'w',encoding='utf-8') as f:
        for item in titles:
            if item.strip().find("Re:") == -1:
                # tmp = re_word.split( item.strip().strip("Fw: ") )
                x =  re_word.match( item.strip().strip("Fw: "))
                if x is not None:
                    if any( True for s in classs if x.group().find(s) is not -1):
                        continue
                    g = re_word.split( item.strip().strip("Fw: ") )
                    # print(count, item, g, x.group())
                    entry = g[-1].replace(",", " ")
                    if x.group().find("[徵才]") is not -1:
                        f.write(entry + "," + str(2) + "\n")
                    else:
                        if any( True for s in keys if g[-1].lower().find(s) is not -1):
                            f.write(entry + "," + str(1)+ "\n")
                        else:
                            f.write(entry + "," + str(0)+ "\n")




def clfTitle():

    titleA = []
    A_label = []
    titleB = []
    keys = [ 'Python', 'Java', '研替', '研發替', 'htc', '華碩', '台積電', '聯發科', 'mtk', 'qnap','offer',
             '群暉', '和碩','華電信', '中鋼', '亞太', '京群', '人資','仁寶', '傑聯特','偉康', '偉嘉','傳媒', '優必達', '優碩','優酷',
             '元大', '兆豐','光寶', '冠信', '凌網', '凌群', '凱信', '凱衛', '凱鈿', '力鯨','創見','勝華','勤崴', '勤業', '南港',
             '台揚','台達電', '啟翔','龍網', '龍騰', '鼎新','鴻佰', '鴻凱', '鴻揚', '鴻海','面試','願境','kkbox','資拓','徵才',
             '感謝函']

    with open("title_c2.csv",'r',encoding='utf-8') as f:
        for row in csv.reader(f,delimiter=','):
            if int(row[1]) == 0:
                titleB.append(preprocess(row[0]))
            else:
                titleA.append( " ".join( jieba.cut( preprocess(row[0]), HMM=False ) ) )
                if titleA[-1].lower().find("windos") != -1:
                    print(titleA[-1])
                A_label.append(int(row[1]))

    titleA.extend(keys)
    A_label.extend([1]*len(keys))
    tfidf = TfidfVectorizer()
    clf = LinearSVC()
    # X = tfidf.fit_transform(titleA)
    # clf.fit(X,A_label)
    # for index in range(0,10):
    #     print(titleB[index], clf.predict(tfidf.transform([" ".join(jieba.cut(titleB[index]))])))

    A = []
    B = []
    X = tfidf.fit_transform(titleA)

    clfA = OneClassSVM(kernel="linear", nu=0.3)
    clfB = OneClassSVM(kernel="linear", nu=0.3)
    clf = OneClassSVM(kernel="linear", nu=0.3)

    for i,item in enumerate(A_label):
        if item == 1:
            A.append(titleA[i])
        else:
            B.append(titleA[i])

    XA = tfidf.transform(A)
    XB = tfidf.transform(B)

    clfA.fit(XA)
    clfB.fit(XB)
    clf.fit(X)

    print(tfidf.get_feature_names())

    # for index in range(0,10):
    #     print([" ".join(jieba.cut(titleB[index]))], clfA.predict(tfidf.transform([" ".join(jieba.cut(titleB[index]))])))
    #     print(titleB[index], clf.predict(tfidf.transform([" ".join(jieba.cut(titleB[index]))])))
    #     print(titleB[index], clfB.predict(tfidf.transform([" ".join(jieba.cut(titleB[index]))])), "\n")

    title = []
    for index in range(960,1000 + 1 ):
        with open(path + str(index) + ".json", 'r',encoding='utf8') as f:
            tmp = json.load(f)
        for item in tmp:
            if item['title'] is not  None:
                title.append(" ".join( jieba.cut( item['title'] ) ) )
    count = 0
    for item in title:
        if clf.predict(tfidf.transform([item]))[0] == -1:
            print( item, )
            count += 1
    print(count,(1000-960)*20)



def preprocess(s):
    s = timeprocess(s)
    s = dateprocess(s)
    s = symbolprocess(s)
    return s

def timeprocess(s):
    return re.sub("([0-1]?[1-9]|2[0-3]\s*)([:|點]\s*)[0-5][0-9]","",s )

def dateprocess(s):
    s = re.sub("([0-9]+\s*(學年|年|/)\s*)?([0-9]+\s*(月|/)\s*)?([0-9]+(\s*日)?)?","",s)
    s = re.sub("[1|2][0-9]{3}[\s*年]?","",s) #西元 1000-2999
    return s

def symbolprocess(s):
    s = re.sub("/"," ", s )
    s = re.sub("[^\w\s]+","",s)
    return s

if __name__ == '__main__':

    # saveTitleOneFile()
    # getFeature()
    # titletoCSV()
    clfTitle()
    # print(symbolprocess("中華電信獎百萬招募Android APP! 4/16說明會缺你不可!"))
    # print(preprocess("宸海科技誠徵Android/JAVA工程師"))