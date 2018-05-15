#-*- coding:utf-8 -*-
"""
    autoscript
    网页抓取方法
    ~~~~~~
    :copyright: (c) 2018 by Taffy.
"""


from selenium import webdriver
from bs4 import BeautifulSoup
import sqlite3
import time
import urlparse
import json
import urllib2


"""
    数据库操作
"""
class Database(object):

    __cursor = None
    __conn = None

    def __init__(self):
        self.__conn = sqlite3.connect('../db/database.db')
        self.__cursor = self.__conn.cursor()


    def execute(self, sql, pars):
        if sql == None:
            return
        print sql
        self.__cursor.execute(sql, pars)
        self.__conn.commit()

    def __del__(self):
        self.__cursor.close()
        self.__conn.close()




def page(url, max = 100000):
    driver = webdriver.Chrome('./chromedriver')
    driver.get(url)

    count = 0
    repeat = 0
    pages = 0

    time.sleep(2)
    while (len(driver.page_source) > count or repeat < 20) and pages <= max :
        if len(driver.page_source) == count:
            repeat = repeat + 1
            print repeat
        else:
            repeat = 0

        count = len(driver.page_source)
        js = "var q=document.documentElement.scrollTop=document.body.scrollHeight"
        driver.execute_script(js)
        pages = pages + 1
        time.sleep(1)

    content = driver.page_source
    driver.quit()

    return content




def yidianzixun():
    # 'https://www.yidianzixun.com/channel/e136117' 痛经
    # 'https://www.yidianzixun.com/channel/w/%E6%9C%88%E7%BB%8F' 痛经
    # 'https://www.yidianzixun.com/channel/c16' 健康
    # 'https://www.yidianzixun.com/channel/c15' 美妆
    # 'https://www.yidianzixun.com/channel/u8867?searchword=%E5%8C%96%E5%A6%86' 美妆
    content = page('https://www.yidianzixun.com/channel/u8867?searchword=%E5%8C%96%E5%A6%86', 10000)
    soup = BeautifulSoup(content)
    newslist = soup.findAll('a', class_ = 'doc')
    db = Database()
    for news in newslist:
        news_id = news.get('data-docid')
        imageTags = news.findAll('img', class_ = 'doc-image')
        titleTag = news.find('div', class_ = 'doc-title')
        sourceName = u'一点资讯'

        subTag = news.find('div', class_ = 'doc-info')
        icoTag = subTag.img
        authorTag = subTag.find('span', class_ = 'source')

        if titleTag == None or subTag == None or icoTag == None or authorTag == None:
            continue

        db.execute("""insert or ignore into news (news_id, title, source_name, source_url, author, read_count, source_ico, type) values(?, ?, ?, ?, ?, ?, ?, ?)""",
                   (news_id, titleTag.string, sourceName, 'www.yidianzixun.com', authorTag.string, 0, 'https:' + icoTag['src'], 4))

        for imgTag in imageTags:
            db.execute("""insert or ignore into image (news_id, url) values(?, ?)""", (news_id, 'https:' + imgTag['src']))

    print '--------------insert count:' + str(len(newslist)) + '-----------------------------------'




def meiyou():
    # https://news.meiyou.com/?category_id=18&sub=2 备孕
    # 'https://news.meiyou.com/?category_id=19&sub=3' 育儿
    # 'https://news.meiyou.com/?category_id=13&sub=7' 美食
    # 'https://news.meiyou.com/?category_id=15&sub=8' 健康
    content = page('https://news.meiyou.com/?category_id=15&sub=8', 10000)
    soup = BeautifulSoup(content)
    articles = soup.findAll('li', class_ = 'item')
    db = Database()

    for article in articles:
        title = article.find('div', class_ = 'pics')
        if title == None:
            continue
        aTag = title.a
        url = 'https://news.meiyou.com' + aTag.get('href')
        query = dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))
        news_id = query['news_id']
        name = aTag.string

        pic = article.find('div', class_ = 'pic-list')
        imgTags = pic.findAll('img')


        source = article.find('div', class_ = 'text-footer')
        sTag = source.a
        iTag = source.i
        if iTag == None:
            read_count = 0
        else:
            read_count = iTag.string

        source_ico = 'https://www.meitu.com/favicon.ico'

        db.execute(
            """insert or ignore into news (news_id, title, source_name, source_url, author, read_count, source_ico, type) values(?, ?, ?, ?, ?, ?, ?, ?)""",
            (news_id, name, u'美柚', 'www.meiyou.com', sTag.string, read_count, '', 5))

        for imgTag in imgTags:
            imgTag
            db.execute("""insert or ignore into image (news_id, url) values(?, ?)""",
                       (news_id, imgTag['src']))


    print '----------------------- insert meiyou count: ' + str(len(articles)) + '  -----------------------------'




def souhu():

    # 'http://v2.sohu.com/public-api/feed?scene=CHANNEL&sceneId=26&page=1&size=1000' 育儿
    # 'http://v2.sohu.com/public-api/feed?scene=TAG&sceneId=70929&page=1&size=1000' 备孕
    # 'http://v2.sohu.com/public-api/feed?scene=CATEGORY&sceneId=1051&page=1&size=1000' 美妆
    # 'http://v2.sohu.com/public-api/feed?scene=CHANNEL&sceneId=24&page=1&size=1000' 健康

    souhu_insert('http://v2.sohu.com/public-api/feed?scene=CHANNEL&sceneId=26&page=1&size=1000', 2)
    souhu_insert('http://v2.sohu.com/public-api/feed?scene=TAG&sceneId=70929&page=1&size=1000', 3)
    souhu_insert('http://v2.sohu.com/public-api/feed?scene=CATEGORY&sceneId=1051&page=1&size=1000', 4)
    souhu_insert('http://v2.sohu.com/public-api/feed?scene=CHANNEL&sceneId=24&page=1&size=1000', 5)

def souhu_insert(url, type):
    rt = urllib2.Request(url)
    rs = urllib2.urlopen(rt)
    content = rs.read().decode('utf-8')
    list = json.loads(content)
    db = Database()
    for item in list:
        if item['authorPic'] != None and len(item['authorPic']) > 10:
            authorURL = 'https:' + item['authorPic']

        news_id = str(item['id']) + '_' + str(item['authorId'])

        db.execute(
            """insert or ignore into news (news_id, title, source_name, source_url, author, read_count, source_ico, type) values(?, ?, ?, ?, ?, ?, ?, ?)""",
            (news_id, item['title'], u'搜狐新闻', 'news.sohu.com', item['authorName'], 0, authorURL, type))

        for img in item['images']:
            # db.execute("""delete from image where news_id = ? """, (item['id'], ))
            db.execute("""insert or ignore into image (news_id, url) values(?, ?)""", (news_id, 'https:' + img))

    print '----------------------- insert souhu count: ' + str(len(list)) + '  -----------------------------'






# yidianzixun()
# meiyou()

souhu()








