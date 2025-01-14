# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import json
import script

SOURCE_HOST = 'news.sohu.com'


def news():
    # 'http://v2.sohu.com/public-api/feed?scene=CHANNEL&sceneId=26&page=1&size=1000' 育儿
    # 'http://v2.sohu.com/public-api/feed?scene=TAG&sceneId=70929&page=1&size=1000' 备孕
    # 'http://v2.sohu.com/public-api/feed?scene=CATEGORY&sceneId=1051&page=1&size=1000' 美妆
    # 'http://v2.sohu.com/public-api/feed?scene=CHANNEL&sceneId=24&page=1&size=1000' 健康

    insert('http://v2.sohu.com/public-api/feed?scene=CHANNEL&sceneId=26&page=1&size=20', 2)
    insert('http://v2.sohu.com/public-api/feed?scene=TAG&sceneId=70929&page=1&size=20', 3)
    insert('http://v2.sohu.com/public-api/feed?scene=CATEGORY&sceneId=1051&page=1&size=20', 4)
    insert('http://v2.sohu.com/public-api/feed?scene=CHANNEL&sceneId=24&page=1&size=20', 5)


def insert(url, type):
    content = script.capture(url)
    list = json.loads(content)
    ids = []
    for item in list:
        title = item['title'].replace("\n", "")
        title = title.strip()
        authorURL = ''
        if item['authorPic'] is not None and len(item['authorPic']) > 10:
            authorURL = 'https:' + item['authorPic']

        news_id = str(item['id']) + '_' + str(item['authorId'])

        script.insert_news(news_id, title, u'搜狐新闻', SOURCE_HOST, item['authorName'], 0, authorURL, type, item['images'])

        if detail(news_id) == 1:
            ids.append(news_id)

    print '----------------------- insert souhu type:' + str(type) + ' count:' + str(
        len(list)) + '  -----------------------------'

    script.appendIDs(ids)


def detail(id):
    if id is None:
        print 'url 不能为 nil'
        return

    content = script.capture('http://www.sohu.com/a/' + str(id))
    if content == "FAIL" or content is None:
        print '内容抓取失败'
        return

    soup = BeautifulSoup(content)
    info = soup.find('div', class_='text')

    if info is None:
        return script.error(id)

    headerTag = info.find('div', class_='text-title')

    titles = headerTag.find('h1').stripped_strings
    for t in titles:
        title = t
        break

    author = u'搜狐新闻'

    try:
        sourceTag = headerTag.find('div', class_='article-info')
        timeTag = sourceTag.find('span', class_='time')
        authorsTag = sourceTag.find('span', class_='tag').findAll('a')
        if len(authorsTag) >= 0:
            author = authorsTag[-1].string
    except:
        pass

    try:
        news_content = info.find('div', class_='article')
        if news_content is None:
            news_content = info.find('article', class_='article')

        news_content.find('span', class_='backword').extract()
        news_content = unicode(news_content).replace("<br/>", "")

        return script.insert_detail(id, title, news_content, author, timeTag.string)
    except:
        return None
