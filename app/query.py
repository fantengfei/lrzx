#-*- coding:utf-8 -*-
"""
    query
    ~~~~~~
    :copyright: (c) 2018 by Taffy.
"""

from autoscript import s_meiyou, s_dayima, s_yidianzixun, s_sohu, script
from db.sql import Database
import random
import threading
import common
import csynonym
import time
import re


def newslist(offset = 0, count = 10, type = 1, PC = True):
    db = Database('newslist')
    if type == 6:
        # 推荐
        re = recommend(offset)
    else:
        re = db.query("""select * from news where type = %d and status = 1 order by create_time desc limit %d offset %d""", (type, count, offset))

    # print '----------------------- query data count: ' + str(len(re)) + ' -------------------------'

    list = manageNews(re, PC)
    random.shuffle(list)
    return list

def hotList(max = 5, type = 6):
    db = Database('hotlist')
    if type != 6:
        re = db.query("""select * from news where type = %d and status = 1 order by read_count desc limit %d offset 0""", (type, max))
    else:
        re = db.query("""select * from news where status = 1 order by read_count desc limit %d offset 0""", (max,))

    list = []
    for news in re:
        news['target'] = common.md5(news['source_url'])
        news['order'] = re.index(news) + 1
        list.append(news)

    return list


def recommend(offset = 0):
    db = Database('recommend')
    re = db.query("""select * from news where status = 1 order by create_time desc, read_count desc limit %d offset %d""", (20, offset))
    return re

def banner():
    db = Database('banner')
    re = db.query("""select * from news where create_time in (select max(create_time) from `news` where status=1 group by type)""")

    list = []
    types = []
    for n in re:
        if n['type'] not in types:
            types.append(n['type'])
            list.append(n)

    return manageNews(list)


def insert_detail(target, id):
    if target == None or id == None:
        return '参数不能为空'

    if target == common.md5(s_meiyou.SOURCE_HOST):
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


def detail(id):
    if id == None:
        return '参数不能为空'

    thread = threading.Thread(target=increase, name='increase', args=(id,))
    thread.start()

    db = Database('detail')
    data = db.query("""select * from detail where news_id = '%s' and status = 1""", (id, ), one=True)
    del db

    if data == None or len(data['content']) < 10:
        return script.error(id)

    p = re.compile('<[^>]+>')
    text = p.sub("", data['content'])
    data['description'] = text[0:150]
    data['description'] = re.sub(u'[\s\r\t\n\d]', '', data['description'])
    data['keywords'] = csynonym.divide(text)
    data['pubDate'] = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
    imgs = common.analysisImgs(data['content'])
    data['imgs'] = imgs[0:3]

    return data


def increase(id):
    db = Database('increase')
    sql = """update news set read_count = read_count + 1 where news_id = '%s'"""
    db.execute(sql, (id,))
    del db


def search(keyword, offset = 0, count = 10, PC = True):
    db = Database('search')
    if keyword == None:
        return []

    newKey = '%'
    for c in keyword:
        newKey = newKey + c + '%'

    re = db.query("""select * from news where title like '%s' and status = 1 order by id desc limit %d offset %d""", (newKey, count, offset))
    # print '----------------------- query data count: ' + str(len(re)) + ' -------------------------'

    list = manageNews(re, PC)

    return list


def manageNews(args = [], PC = True):
    db = Database('manageNews')
    if len(args) == 0:
        return args

    haveFullStyle = False
    list = []
    for news in args:
        news['is_pc'] = PC
        imgs = db.query("""select url from image where news_id = '%s'""", (news['news_id'],))
        srcs = []

        for img in imgs:
            srcs.append(img['url'])

        rdm = random.randint(0, 9)
        length = len(srcs)

        if PC:
            count = 1 if length < 4 else 4
            if rdm % 2 == 0 and news['summary'] != None and haveFullStyle == False:
                haveFullStyle = True
                count = 2
        else:
            count = 3
            if rdm % 2 == 0 and news['summary'] != None and haveFullStyle == False:
                haveFullStyle = True
                count = 2

        news['imgs'] = srcs[:count]
        list.append(news)

    return list


def auto_script():
    global timer
    timer = threading.Timer(60 * 60 * 6, auto_script_helper)
    timer.start()


def auto_script_helper():
    capture()
    auto_script()

def capture():
    # s_dayima.news()
    # s_meiyou.news()
    s_sohu.news()
    s_yidianzixun.news()
    script.post_tongji()


def test(retry = None):
    db = Database('test')
    if retry == None:
        sql = "select * from news where status = 1"
    else:
        sql = "select * from news where status = 1 and news_id not in (select news_id from detail)"

    re = db.query(sql)
    del db

    for news in re:
        print insert_detail(common.md5(news['source_url']), news['news_id'])

    return '<center><h1> %d </h1></center>' % len(re)
