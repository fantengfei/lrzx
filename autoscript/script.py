#-*- coding:utf-8 -*-
"""
    autoscript
    脚本的基础方法
    ~~~~~~
    :copyright: (c) 2018 by Taffy.
"""

import requests
# import cookielib
# import  urllib, urllib2
from db.sql import Database


def insert_news(news_id, title, source_name, source_url, author, count, ico, type, imgs):
    db = Database()
    re = db.execute("insert or ignore into news (news_id, title, source_name, source_url, author, read_count, source_ico, type) \
                        values('%s', '%s', '%s', '%s', '%s', %d, '%s', '%d')" % \
                        (news_id, title, source_name, source_url, author, count, ico, type))

    for img in imgs:
        if img.find('https:') != 0 and img.find('http:') != 0:
            img = 'https:' + img

        db.execute("insert or ignore into image (news_id, url) values('%s', '%s')" % (news_id, img))

    return re


def capture(url, headers = None):
    if url == None:
        return None

    re = requests.get(url, params=None, headers=headers)

    # rt = urllib2.Request(url, None, headers)
    # rt = urllib2.Request(url)
    # rs = urllib2.urlopen(rt)
    # content = rs.read().decode('utf-8')

    return re.text


def error():
    return {'title': '', 'time': '', 'source': '', 'content': u'<center>出错了！文章可能被下架了哦~</center>'}

