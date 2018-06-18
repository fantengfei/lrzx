#-*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import json
import script

SOURCE_HOST = 'www.meiyou.com'

def news():
    # 大姨妈
    insert(script.capture('https://news.meiyou.com/news-api/v2/web_news_more?category_id=16'), 1)
    # 备孕
    insert(script.capture('https://news.meiyou.com/news-api/v2/web_news_more?category_id=18'), 2)
    # 育儿
    insert(script.capture('https://news.meiyou.com/news-api/v2/web_news_more?category_id=19'), 3)
    # 美妆
    insert(script.capture('https://news.meiyou.com/news-api/v2/web_news_more?category_id=8'), 4)
    # 健康
    insert(script.capture('https://news.meiyou.com/news-api/v2/web_news_more?category_id=15'), 5)

    # URL = 'https://news.meiyou.com/?category_id=16&sub=1'
    #
    # if content == "FAIL" or content == None:
    #     # sql = "UPDATE QUESTION SET LAST_VISIT = %s WHERE LINK_ID = %s"
    #     # self.cursor.execute(sql,(time_now,link_id))
    #     return 'invalid path'
    #
    # soup = BeautifulSoup(content)
    # articles = soup.findAll('li', class_ = 'item')
    #
    # for article in articles:
    #     title = article.find('div', class_ = 'pics')
    #     aTag = title.a
    #     url = 'https://news.meiyou.com' + aTag.get('href')
    #     query = dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))
    #     news_id = query['news_id']
    #     name = aTag.string
    #
    #     pic = article.find('div', class_ = 'pic-list')
    #     imgTag = pic.img
    #
    #
    #     source = article.find('div', class_ = 'text-footer')
    #     sTag = source.a
    #     iTag = source.i
    #     if iTag == None:
    #         read_count = 0
    #     else:
    #         read_count = iTag.string
    #
    #     source_ico = 'https://www.meitu.com/favicon.ico'
    #
    #     query_db(
    #         'insert or ignore into news (news_id, url, title, img, source_name, source_url, author, read_count, source_ico) values(?, ?, ?, ?, ?, ?, ?, ?, ?)',
    #         [news_id, url, name, imgTag['src'], u'\u7f8e\u67da', SOURCE_HOST, sTag.string, read_count, source_ico],
    #         one=True)
    #
    #
    # print 'insert finished'

    # news_detail = 'https://news.meiyou.com/news_detail?news_id={news_id}&category_id=16&detail_id=16&sub=1'
    # source_ico = 'https://static.seeyouyima.com/www.meiyou.com/meiyou-bf23e296a9058a8dd5581eda3ea59674.png'


def insert(content, type):
    list = json.loads(content)
    source_ico = ''
    ids = []
    for news in list['data']['feeds']:
        author = news['author'].replace("\n", "")
        author = author.strip()
        title = news['title'].replace("\n", "")
        title = title.strip()

        imgs = []
        for img in news['images']:
            imgs.append(img['src'])
        script.insert_news(news['id'], title, u'美柚', SOURCE_HOST, author, 0, source_ico, type, imgs)

        if detail(news['id']) == 1:
            ids.append(news['id'])



    print '----------------------- insert meiyou type '+str(type)+' count: ' + str(len(list)) + '  -----------------------------'

    script.appendIDs(ids)



def detail(id):
    if id == None:
        print 'url 不能为 nil'
        return

    content = script.capture('https://news.meiyou.com/news_detail?news_id=' + str(id))
    content = content.replace('</html>', '')
    if content == "FAIL" or content == None:
        return '内容抓取失败'

    soup = BeautifulSoup(content)
    info = soup.find('div', class_ = 'warp')

    if info == None:
        return script.error(id)

    warp_title = info.find('div', class_ = 'warp-title')
    news_content = info.find('div', class_ = 'news-content')
    news_content = unicode(news_content).replace("<br/>", "")

    title = warp_title.h2
    time = warp_title.find('span', class_ = 'n-time')
    sources = warp_title.findAll('span')

    return script.insert_detail(id, title.string, news_content, sources[-1].string, time.string)

