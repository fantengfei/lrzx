#-*- coding:utf-8 -*-


from bs4 import BeautifulSoup
import script

SOURCE_HOST = 'http://www.dayima.com'

# http://www.dayima.com/articles
# http://www.dayima.com/articles/article/1011


def news():
    url = 'http://www.dayima.com/articles'
    content = script.capture(url)

    if content == "FAIL" or content == None:
        return 'invalid path'

    soup = BeautifulSoup(content)
    articles = soup.findAll('div', class_ = 'dotted')

    for article in articles:
        title = article.find('div', class_ = 'title')
        aTag = title.a

        url = aTag.get('href')
        name = aTag.string

        query = url.split('/')
        news_id = query[-1]


        pic = article.find('div', class_ = 'picArea')
        imgTag = pic.img

        read_count = 0
        source_name = u'大姨妈'
        source_ico = ''

        script.insert_news(news_id, name, source_name, SOURCE_HOST, '', read_count, source_ico, 1, (imgTag['src'],))

        detail(news_id)

    print '----------------------- insert dayima count: ' + str(len(articles)) + '  -----------------------------'


def detail(id):
    if id == None:
        print 'url 不能为 nil'
        return

    content = script.capture('http://www.dayima.com/articles/article/' + id)

    if content == "FAIL" or content == None:
        return '内容抓取失败'

    soup = BeautifulSoup(content)
    info = soup.find('div', class_ = 'leftArea')
    if info == None:
        return script.error(id)

    titleTag = info.find('div', class_ = 'artilce_title')
    newsContent = info.find('div', class_ = 'article_content')
    newsContent = unicode(newsContent).replace("<br/>", "  ")
    bref = unicode(info.find('div', class_ = 'article_brief')).replace("<br/>", " ")

    title = titleTag.string
    time = info.find('span', class_ = 'artilce_time')
    sources = u'大姨妈'

    # print title.string + '-' + time.string

    # data = {'title': title, 'time': time.string, 'source': sources, 'content': bref + newsContent}

    script.insert_detail(id, title, bref + newsContent, sources, time.string)

