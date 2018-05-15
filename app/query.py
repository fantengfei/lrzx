#-*- coding:utf-8 -*-
"""
    query
    ~~~~~~
    :copyright: (c) 2018 by Taffy.
"""

from autoscript import  s_meiyou
from autoscript import  s_dayima
from autoscript import  s_yidianzixun
from autoscript import  s_sohu
from db.sql import query_db
import random
from threading import Timer

def newslist(offset = 0, count = 10, type = 1, PC = True):
    if type == 6:
        re = recommend(offset)
    else:
        re = query_db('select * from news where type = ? order by id desc limit ? offset ?', [type, count, offset], one=False)

    # print '----------------------- query data count: ' + str(len(re)) + ' -------------------------'

    list = manageNews(re, PC)
    random.shuffle(list)
    return list

def hotList(max = 5, type = 1):
    if type != 6:
        re = query_db('select * from news where type = ? order by read_count desc limit ? offset 0', [type, max], one=False)
    else:
        re = query_db('select * from news order by read_count desc limit ? offset 0', [max], one=False)

    list = []
    for news in re:
        news['target'] = __md5(news['source_url'])
        news['order'] = re.index(news) + 1
        list.append(news)

    return list


def recommend(offset = 0):
    re = query_db('select * from news order by read_count desc , create_time asc limit ? offset ?', (20, offset), one=False)
    return re

def detail(target, id):
    if target == None or id == None:
        return '参数不能为空'

    # read_count + 1
    query_db('update news set read_count = read_count + 1 where news_id = ?', [id])

    if target == __md5(s_meiyou.SOURCE_HOST):
        content = s_meiyou.detail(id)
        return content

    if target == __md5(s_dayima.SOURCE_HOST):
        content = s_dayima.detail(id)
        return content

    if target == __md5(s_yidianzixun.SOURCE_HOST):
        content = s_yidianzixun.detail(id)
        return content

    if target == __md5(s_sohu.SOURCE_HOST):
        content = s_sohu.detail(id)
        return content


    return '未能匹配到 target'

def search(keyword, offset = 0, count = 10, PC = True):
    if keyword == None:
        return []

    newKey = '%'
    for c in keyword:
        newKey = newKey + c + '%'

    re = query_db("select * from news where title like ? order by id desc limit ? offset ?", ['%' + newKey + '%', count, offset], one=False)
    # print '----------------------- query data count: ' + str(len(re)) + ' -------------------------'

    list = manageNews(re, PC)

    return list




def manageNews(args = [], PC = True):
    if len(args) == 0:
        return args

    list = []
    for news in args:
        news['target'] = __md5(news['source_url'])
        imgs = query_db('select url from image where news_id = ?', [news['news_id']], one=False)
        srcs = []
        for img in imgs:
            srcs.append(img['url'])

        if PC:
            count = 1 if len(srcs) < 4 else 4
        else:
            count = 3
        news['imgs'] = srcs[:count]
        list.append(news)

    return list


def auto_script():
    s_meiyou.news()
    s_dayima.news()
    s_sohu.news()
    s_yidianzixun.news()

    Timer(60 * 60 + 6, auto_script, ()).start()


def test():
    return s_yidianzixun.news()


def __md5(str):
    import hashlib
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()