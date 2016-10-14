# -*- coding: utf-8 -*-
import json
import re

import jieba
# jieba.analyse.set_stop_words("../data/stop_words.txt")
# jieba.analyse.set_idf_path("../data/idf.txt.big.txt")
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.svm import OneClassSVM

jieba.load_userdict("../data/userdict.txt")
jieba.add_word("版上")
jieba.add_word('人資')
jieba.suggest_freq('版上', True)
jieba.suggest_freq('人資', True)


import jieba.analyse
import xlrd
import xlsxwriter
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.svm import SVC


path = "../soft_data/"
start = 954
end = 954+10


title = []





keywords = [ '徵才', 'Python', 'Java', '研替', '研發替', 'htc', '華碩', '台積電', '聯發科', 'mtk', 'qnap',  ]

re_word = re.compile("\[[\u4e00-\u9fa5]*\]")

def write_data():
    workbook = xlsxwriter.Workbook('title2.xlsx')
    worksheet = workbook.add_worksheet()
    count = 1

    for index in range(start, end + 1 ):
        with open( path + str(index) + ".json", 'r',encoding='utf-8') as f:
            article_list = json.load(f)

        # title.extend( [ item['title'] for item in article_list ] )
        # print(*title,sep='\n')
        title = []
        # print(index)
        for item in article_list:
            if item['title'] is not None:
                if item['title'].find('徵') != -1:
                    # strx = item['title'].strip().strip("Re: |Fw: ")
                    # g = re_word.split(strx)
                    # if len(g) == 2:
                    #     worksheet.write("A"+str(count), g[1].strip().lower())
                    #     worksheet.write("B"+str(count), 1)
                    #     count += 1
                    # donothing
                    pass
                else:
                    strx = item['title'].strip().strip("Re: |Fw: ")
                    g = re_word.split(strx)
                    if len(g) == 2:
                        worksheet.write("A"+str(count), g[1].strip().lower())
                        count += 1



    workbook.close()

# with open( path + str(1062) + ".json", 'r',encoding='utf-8') as f:
#     article_list = json.load(f)
#     for item in article_list:
#         print(item['title'])

def handler_data():
    book = xlrd.open_workbook("title.xlsx")
    workbook = book.sheet_by_index(0)



    title_array = []
    cla_array = []
    # jieba.load_userdict("../data/userdict.txt")
    jieba.add_word("版上")
    jieba.add_word('人資')
    jieba.suggest_freq('版上', True)
    jieba.suggest_freq('人資', True)
    jieba.del_word('時人')
    jieba.suggest_freq('時人', False)
    jieba.initialize()
    # print(" /".join(jieba.cut("版上有從前端轉到後端的朋友嗎?")))
    # print(" /".join(jieba.cut("面試時人資的問題",HMM=False )))

    for rx in range(0,100):
        tmp = workbook.row(rx)
        # if int(tmp[1].value) == 1:
        title_array.append(" ".join(jieba.lcut(tmp[0].value)) )
        cla_array.append(int(tmp[1].value))


    test_title = []
    testcla = []

    for rx in range(100,150):
        tmp = workbook.row(rx)
        test_title.append(" ".join(jieba.lcut(tmp[0].value)))
        testcla.append( int(tmp[1].value) )


    # classifier = Pipeline([
    #     ('vectorizer', CountVectorizer()),
    #     ('tfidf', TfidfTransformer()),
    #     ('clf', SGDClassifier())])

    # classifier.fit(title_array,cla_array)
    # print( test_title[0] )
    # print( classifier.predict(test_title[0]), testcla[0] )

    with open("../data/stop_words.txt",'r',encoding='utf8') as f:
        stopwords = f.read().split('\n')


    cvec = CountVectorizer()
    tfidf = TfidfVectorizer(analyzer='word', stop_words=stopwords)
    clf = SVC(C=1000000.0, gamma='auto', kernel='rbf',verbose=False,probability=True)
    # clf = SGDClassifier()
    # clf = OneVsRestClassifier(LinearSVC(random_state=0))
    # clf = OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
    X = tfidf.fit_transform(title_array)
    print(X.shape)
    clf.fit(X,cla_array)
    X_test = tfidf.transform(test_title[0])


    for i,item in enumerate(test_title):
        g = clf.predict(tfidf.transform([item]))
        print(g, testcla[i],item)

    # with open("feature Name.csv",'w') as f:
    #     f.write("word\n")
    #     for item in tfidf.get_feature_names():
    #         f.write(item + "\n")




handler_data()