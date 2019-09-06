#-*- coding:utf-8 -*-
"""
    adminQuery
    ~~~~~~
    :copyright: (c) 2018 by Taffy.
"""

from autoscript import script
from db.sql import Database
import common
import json

def verify_user(username, password):
    db = Database('verify_user')
    re = db.query("""select password from account where number='%s' and status = 1 """, (username,), True)
    if re and re.has_key('password') and re['password'] == common.md5(password):
        return True

    return False


def analysisURL(url):
    import requests
    from readability import Document

    html = requests.get(url)
    text = html.text
    text = text.replace('</html>', '')

    article = Document(text).summary()
    title = Document(text).short_title()

    data = {"content": article, "title": title}
    return json.dumps(data)


def add_news(title, content, imgs, type, username):
    import uuid
    news_id = str(uuid.uuid1())

    db = Database('add_news')
    user = db.query("""select nickname from account where number='%s' and status=1""", (username, ), True)
    del db

    imgs = imgs.split(',')
    re = script.insert_news(news_id, title, u'丽人资讯', 'lrzx.somenews.cn', user['nickname'], 0, '', int(type), imgs)
    if re == 1:
        dre = script.insert_detail(news_id, title, content, user['nickname'], '')
        if dre == 1:
            script.appendIDs((news_id, ))
            script.post_tongji()
            return news_id

    return False

