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
import os
from app.csynonym import recombination

def insert_news(news_id, title, source_name, source_url, author, count, ico, type, imgs, summary = ''):
    db = Database('insert')
    sql = """insert ignore into news (news_id, title, source_name, source_url, author, read_count, source_ico, type, summary) values('%s', '%s', '%s', '%s', '%s', %d, '%s', '%d', '%s')"""
    re = db.execute(sql, par=(news_id, recombination(title), source_name, source_url, author, count, ico, type, summary))

    for img in imgs:
        if len(img) < 5:
            continue

        if img.find('https:') != 0 and img.find('http:') != 0:
            img = 'https:' + img

        db.execute("""insert ignore into image (news_id, url) values('%s', '%s')""", par=(news_id, img))
    return re


def insert_detail(news_id, title, content, source, publishTime):
    db = Database('detail')
    sql = """insert ignore into detail (news_id, title, content, source, publish_time) values('%s', '%s', '%s', '%s', '%s')"""
    re = db.execute(sql, par=(news_id, recombination(title), recombination(content), source, publishTime))
    return re

def capture(url, headers = None):
    if url == None:
        return None

    re = requests.get(url, params=None, headers=headers)
    return re.text


def error(news_id=None):
    info = {'title': '', 'publish_time': '', 'source': '', 'content': u'<center>出错了！文章可能被下架了哦~</center>'}
    if news_id == None:
        return info
    thread = threading.Thread(target=delete, name='error', args=(news_id,))
    thread.start()
    return info


def delete(news_id):
    db = Database('error')
    sql = """update news set status = -1 where news_id = '%s'"""
    db.execute(sql, (news_id,))
    del db



def post_tongji():
    import requests

    urls = {'file': open('urls.txt', 'rb')}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post('http://data.zz.baidu.com/urls?site=https://www.somenews.cn&token=SBa14K60QlnF0nz5', files=urls, headers=headers)

    os.remove('urls.txt')


def appendIDs(ids=[]):
    path = 'urls.txt'
    if os.path.exists(path) == False:
        file = open(path, 'w')
    else:
        file = open(path, 'a')

    for id in ids:
        file.write(__generateURL(id))
    file.close()


def __generateURL(id):
    return 'https://www.somenews.cn/detail/' + str(id) + '\n'