#-*- coding:utf-8 -*-


from bs4 import BeautifulSoup
import script
import json

SOURCE_HOST = 'www.yidianzixun.com'

# https://www.yidianzixun.com/channel/e136117 大姨妈

def news():
    re = None

    dayima = 'https://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=e136117&cstart=0&cend=10&infinite=true&refresh=1'
    cookie = 'sptoken=Uo%3B9%3C%3B%3B%3DU%3AU%3B%3AU48261efeced332cc9f20413132c69381055d716a322357935f2644077f81ee1b;'
    re = insert(dayima, 1, cookie)

    yuer = 'https://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=t1020&cstart=0&cend=10&infinite=true&refresh=1'
    cookie = 'sptoken=U~%3B%3A8%3AU%3AU%3B%3AU48261efeced332cc9f20413132c69381055d716a322357935f2644077f81ee1b;'
    re = insert(yuer, 2, cookie)

    beiyun = 'https://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=u7682&cstart=0&cend=10&infinite=true&refresh=1'
    cookie = 'sptoken=U%7F%3D%3C28U%3AU%3B%3AU48261efeced332cc9f20413132c69381055d716a322357935f2644077f81ee1b;'
    re = insert(beiyun, 3, cookie)

    meizhuang = 'https://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=u8867&cstart=0&cend=10&infinite=true&refresh=1'
    cookie = 'sptoken=U%7F22%3C%3DU%3AU%3B%3AU48261efeced332cc9f20413132c69381055d716a322357935f2644077f81ee1b;'
    re = insert(meizhuang, 4, cookie)

    jiangkang = 'https://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=11968972663&cstart=0&cend=10&infinite=true&refresh=1'
    cookie = 'wuid=115726917722451; wuid_createAt=2018-04-23 19:44:9; UM_distinctid=162f2518a1a8d5-09f8a8bac82f9b-33657106-1aeaa0-162f2518a1b17f; JSESSIONID=70631c5e111d0524de72e1c6a87b181612b7de36a0671790909c451ff3ae3f83; DID=f6c4fcaaac844b8dbcff05db50b07db2d3d1310cbda7afe54f7256ee3a024ab9; weather_auth=2; Hm_lvt_15fafbae2b9b11d280c79eff3b840e45=1526186052,1526268689,1526293285,1526293314; CNZZDATA1255169715=895922743-1524481024-https%253A%252F%252Fwww.google.com.hk%252F%7C1526353454; sptoken=U%3B%3B3%3C23%3D8%3C%3C9U%3AU%3B%3AU48261efeced332cc9f20413132c69381055d716a322357935f2644077f81ee1b; Hm_lpvt_15fafbae2b9b11d280c79eff3b840e45=1526357646; captcha=s%3A6e4b5d307629c2f146a68d0e834dd8eb.AXON%2F9VN3VCSQMyEgjdwH4mNZK82PQELeZUJ4IsgEbI; cn_1255169715_dplus=%7B%22distinct_id%22%3A%20%22162f2518a1a8d5-09f8a8bac82f9b-33657106-1aeaa0-162f2518a1b17f%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201526357651%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201526357651%7D%7D'
    re = insert(jiangkang, 5, cookie)



def insert(url, type, cookie):
    headers = {
        'Referer': 'https://www.yidianzixun.com/channel/e136117',
        'cookie': cookie
    }

    content = script.capture(url, headers)
    content = json.loads(content)

    if content.has_key('result') == False:
        return

    for news in content['result']:
        if news.has_key('content_type') != True or news['content_type'] != 'news':
            continue
        news_id = news['itemid']
        title = news['title'].replace("\n", "")
        title = title.strip()
        sourceName = u'一点资讯'
        author = news['source']

        ico = ''
        if news.has_key('wemedia_info') and news['wemedia_info'].has_key('image'):
            ico = news['wemedia_info']['image']

        imgs = []
        if news.has_key('image_urls') == True:
            for img in news['image_urls']:
                imgs.append('https://i1.go2yd.com/image.php?type=thumbnail_336x216&url=' + img)

        if title == None or news_id == None:
            continue

        script.insert_news(news_id, title, sourceName, SOURCE_HOST, author, 0, ico, type, imgs)

    print '--------------insert yidianzixun type:'+str(type)+' count:' + str(len(content['result'])) + '-----------------------------------'


def detail(id):
    content = script.capture('https://www.yidianzixun.com/article/' + id)
    soup = BeautifulSoup(content)

    wrapperTag = soup.find('div', class_ = 'left-wrapper')
    if wrapperTag == None:
        return script.error()

    titleTag = wrapperTag.h2
    if titleTag == None:
        return script.error()

    metaTag = wrapperTag.find('div', class_ = 'meta')
    sourceTag = metaTag.a
    timeTag = metaTag.span

    detail = wrapperTag.find('div', class_ = 'content-bd')
    if detail == None:
        detail = wrapperTag.find('div', class_ = 'video-wrapper')

    return {'title': titleTag.string, 'time': timeTag.string, 'source': sourceTag.string, 'content': detail}
