#-*- coding:utf-8 -*-
"""
    autoscript
    脚本的基础方法
    ~~~~~~
    :copyright: (c) 2018 by Taffy.
"""

import requests
from db.sql import Database
import threading

def insert_news(news_id, title, source_name, source_url, author, count, ico, type, imgs):
    db = Database('insert')
    re = db.execute("insert ignore into news (news_id, title, source_name, source_url, author, read_count, source_ico, type) \
                        values('%s', '%s', '%s', '%s', '%s', %d, '%s', '%d')" % \
                        (news_id, title, source_name, source_url, author, count, ico, type))

    for img in imgs:
        if img.find('https:') != 0 and img.find('http:') != 0:
            img = 'https:' + img

        db.execute("insert ignore into image (news_id, url) values('%s', '%s')" % (news_id, img))
    return re


def capture(url, headers = None):
    if url == None:
        return None

    re = requests.get(url, params=None, headers=headers)
    return re.text


def error(news_id=None):
    info = {'title': '', 'time': '', 'source': '', 'content': u'<center>出错了！文章可能被下架了哦~</center>'}
    if news_id == None:
        return info
    thread = threading.Thread(target=delete, name='error', args=(news_id,))
    thread.start()
    return info


def delete(news_id):
    db = Database('error')
    sql = "update news set status = -1 where news_id = '%s'" % news_id
    db.execute(sql)
    del db