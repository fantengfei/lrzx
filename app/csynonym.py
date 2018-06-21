#-*- coding:utf-8 -*-
"""
    common
    ~~~~~~
    :copyright: (c) 2018 by Taffy.
"""

import synonyms
import re

__CIKU = {}

# 分词
# 返回以逗号分开的名词字符串
def divide(str):
    re = synonyms.seg(str)
    danci = re[0]
    cixing = re[1]

    keywords = []

    for index in range(len(danci)):
        if cixing[index].startswith('n') or cixing[index].startswith('v'):
            if len(danci[index]) > 1:
                keywords.append(danci[index])

    keywords = list(set(keywords))

    return ','.join(keywords)


# 重新组合句子
def recombination(sentence):
    if len(__CIKU) == 0:
        __analysis_ciku()

    re = synonyms.seg(sentence)

    cixing = re[1]
    danci = re[0]

    filer = [u'x', u'm']

    newStr = ''

    for index in range(len(danci)):
        newc = danci[index].encode('utf-8')
        if cixing[index] not in filer:
            if __CIKU.has_key(newc):
                newc = __CIKU[newc]
            # else:
            #     ncx = synonyms.nearby(newc)
            #     nc = ncx[0]
            #     if len(nc) > 1:
            #         newc = nc[1]

        newStr = newStr + newc

    return newStr


# 解析词库
def __analysis_ciku():
    file = open('synonym.csv', 'rb')
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


