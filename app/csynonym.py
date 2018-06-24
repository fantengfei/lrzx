#-*- coding:utf-8 -*-
"""
    common
    ~~~~~~
    :copyright: (c) 2018 by Taffy.
"""

# import jieba
# import jieba.analyse
from yaha import Cuttor
from yaha.analyse import extract_keywords, summarize1
import re
import os

__CIKU = {}
cuttor = Cuttor()

# 分词
# 返回以逗号分开的名词字符串
def divide(str):
    keys = extract_keywords(unicode(str))
    return ','.join(keys[0:20])


# 重新组合句子
def recombination(sentence):
    if len(__CIKU) == 0:
        __analysis_ciku()

    seglist = cuttor.cut(unicode(sentence))

    newStr = ''

    for ci in list(seglist):
        newc = ci.encode('utf-8')
        if __CIKU.has_key(newc):
            newc = __CIKU[newc]

        newStr = newStr + newc

    return unicode(newStr, 'utf-8')


# 解析词库
def __analysis_ciku():
    current_path = os.path.abspath(__file__)
    path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
    file = open(path + '/synonym.csv', 'rb')
    for line in file:
        ar = line.split(',')

        for index in range(len(ar)):
            ar[index] = re.sub(u'[\r\t\n\d]', '', ar[index])

        while '' in ar:
            ar.remove('')

        if len(ar) >= 2:
            __CIKU[ar[0]] = ar[1]
            __CIKU[ar[1]] = ar[0]

    file.close()


