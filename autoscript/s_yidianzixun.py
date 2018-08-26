#-*- coding:utf-8 -*-


from bs4 import BeautifulSoup
import script
import json

SOURCE_HOST = 'www.yidianzixun.com'

def news():
    re = None

    dayima = 'https://www.yidianzixun.com/home/q/news_list_for_keyword?display=%E6%9C%88%E7%BB%8F%20%E5%A4%A7%E5%A7%A8%E5%A6%88&cstart=0&cend=20&word_type=token&multi=5&appid=web_yidian&_=1535295188731'
    re = insert(dayima, 1)

    yuer = 'https://www.yidianzixun.com/home/q/news_list_for_keyword?display=%E5%A4%87%E5%AD%95&cstart=0&cend=20&word_type=token&multi=5&appid=web_yidian&_=1535295260779'
    re = insert(yuer, 2)

    beiyun = 'https://www.yidianzixun.com/home/q/news_list_for_keyword?display=%E8%82%B2%E5%84%BF&cstart=0&cend=20&word_type=token&multi=5&appid=web_yidian&_=1535295307179'
    re = insert(beiyun, 3)

    meizhuang = 'https://www.yidianzixun.com/home/q/news_list_for_keyword?display=%E5%81%A5%E5%BA%B7%20%E5%85%BB%E7%94%9F&cstart=0&cend=20&word_type=token&multi=5&appid=web_yidian&_=1535295356090'
    re = insert(meizhuang, 4)

    jiangkang = 'https://www.yidianzixun.com/home/q/news_list_for_keyword?display=%E7%BE%8E%E5%A6%86%20%E6%97%B6%E5%B0%9A%20%E5%8C%96%E5%A6%86%20%E7%BE%8E%E5%A5%B3&cstart=0&cend=10&word_type=token&multi=5&appid=web_yidian&_=1535295497638'
    re = insert(jiangkang, 5)



def insert(url, type, cookie=''):
    headers = {
        'Referer': 'https://www.yidianzixun.com/channel/e136117',
        'cookie': 'JSESSIONID=5b833bbd91a7574bbfed3af92d4b4817966f7198e7c2845b95639ad32dc64e3c;',
        'content-type':	'application/json; charset=utf-8'
    }

    try:
        content = script.capture(url, headers)
        content = json.loads(content)
    except:
        print url + ": 解析失败"
        return

    if content.has_key('result') == False:
        return

    ids = []

    for news in content['result']:
        if news.has_key('content_type') != True or news['content_type'] != 'news':
            continue
        news_id = news['itemid']
        title = news['title'].replace("\n", "")
        title = title.strip()
        sourceName = u'一点资讯'
        author = news['source']
        summary = news['summary']

        ico = ''
        if news.has_key('wemedia_info') and news['wemedia_info'].has_key('image'):
            ico = news['wemedia_info']['image']

        imgs = []
        if news.has_key('image_urls') == True:
            for img in news['image_urls']:
                imgs.append('https://i1.go2yd.com/image.php?type=thumbnail_336x216&url=' + img)

        if title == None or news_id == None:
            continue

        script.insert_news(news_id, title, sourceName, SOURCE_HOST, author, 0, ico, type, imgs, summary)

        if detail(news_id) == 1:
            ids.append(news_id)

    print '--------------insert yidianzixun type:'+str(type)+' count:' + str(len(content['result'])) + '-----------------------------------'

    script.appendIDs(ids)


def detail(id):
    content = script.capture('https://www.yidianzixun.com/article/' + id)
    soup = BeautifulSoup(content)

    wrapperTag = soup.find('div', class_ = 'left-wrapper')
    if wrapperTag == None:
        return script.error(id)

    titleTag = wrapperTag.h2
    if titleTag == None:
        return script.error(id)

    metaTag = wrapperTag.find('div', class_ = 'meta')
    sourceTag = metaTag.a
    timeTag = metaTag.span

    detail = wrapperTag.find('div', class_ = 'content-bd')
    if detail == None:
        detail = wrapperTag.find('div', class_ = 'video-wrapper')

    return script.insert_detail(id, titleTag.string, detail, sourceTag.string, timeTag.string)