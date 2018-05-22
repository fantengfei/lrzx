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
from db.sql import Database
import random
import threading



def newslist(offset = 0, count = 10, type = 1, PC = True):
    db = Database('newslist')
    if type == 6:
        # 推荐
        re = recommend(offset)
    else:
        re = db.query("select * from news where type = %d and status = 1 order by create_time desc limit %d offset %d" % (type, count, offset))

    # print '----------------------- query data count: ' + str(len(re)) + ' -------------------------'

    list = manageNews(re, PC)
    random.shuffle(list)
    return list

def hotList(max = 5, type = 6):
    db = Database('hotlist')
    if type != 6:
        re = db.query('select * from news where type = %d and status = 1 order by read_count desc limit %d offset 0' % (type, max))
    else:
        re = db.query('select * from news where status = 1 order by read_count desc limit %d offset 0' % (max,))

    list = []
    for news in re:
        news['target'] = __md5(news['source_url'])
        news['order'] = re.index(news) + 1
        list.append(news)

    return list


def recommend(offset = 0):
    db = Database('recommend')
    re = db.query('select * from news where status = 1 order by create_time desc, read_count desc limit %d offset %d' % (20, offset))
    return re

def detail(target, id):
    if target == None or id == None:
        return '参数不能为空'

    thread = threading.Thread(target=increase, name='increase', args=(id,))
    thread.start()

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

def increase(id):
    db = Database('increase')
    sql = 'update news set read_count = read_count + 1 where news_id = "%s"' % (id,)
    db.execute(sql)
    del db

def search(keyword, offset = 0, count = 10, PC = True):
    db = Database('search')
    if keyword == None:
        return []

    newKey = '%'
    for c in keyword:
        newKey = newKey + c + '%'

    re = db.query("select * from news where title like '%s' and status = 1 order by id desc limit %d offset %d" % (newKey, count, offset))
    # print '----------------------- query data count: ' + str(len(re)) + ' -------------------------'

    list = manageNews(re, PC)

    return list




def manageNews(args = [], PC = True):
    db = Database('manageNews')
    if len(args) == 0:
        return args

    list = []
    for news in args:
        news['target'] = __md5(news['source_url'])
        imgs = db.query('select url from image where news_id = "%s"' % (news['news_id'],))
        srcs = []

        for img in imgs:
            srcs.append(img['url'])

        rdm = random.randint(0, 9)
        length = len(srcs)

        if PC:
            count = 1 if length < 4 else 4
            if length == 2 or (rdm % 3 == 0 and length == 3):
                count = 2
        else:
            count = 3
            if length == 2 or rdm % 3 == 0:
                count = 2
        news['imgs'] = srcs[:count]
        list.append(news)

    return list


def auto_script():
    s_meiyou.news()
    s_dayima.news()
    s_sohu.news()
    s_yidianzixun.news()

    global timer
    timer = threading.Timer(60 * 60 * 6, auto_script)
    timer.start()


def test():
    return s_yidianzixun.news()


def __md5(str):
    import hashlib
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()