# -*- coding: utf-8 -*-
"""
    index
    ~~~~~~
    :copyright: (c) 2018 by Taffy.
"""

from flask import Flask, request, redirect, url_for, render_template
from app import query
from admin import admin_api

app = Flask(__name__)
app.debug = True
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?R/LJDHCS/,/s'
app.register_blueprint(admin_api)

@app.route('/')
@app.route('/home')
def index():
    return render_template('front/index.html', list=query.newslist(type = 6, PC = __ISPC()), hots=query.hotList(type=6), banners=query.banner())

@app.route('/dayima')
def dayima():
    return render_template('front/dayima.html', list=query.newslist(type = 1, PC=__ISPC()), hots=query.hotList(type=1))

@app.route('/education')
def education():
    return render_template('front/education.html', list=query.newslist(type=2, PC=__ISPC()), hots=query.hotList(type=2))

@app.route('/beiyun')
def beiyun():
    return render_template('front/beiyun.html', list=query.newslist(type=3, PC=__ISPC()), hots=query.hotList(type=3))

@app.route('/meizhuang')
def meizhuang():
    return render_template('front/meizhuang.html', list=query.newslist(type=4, PC=__ISPC()), hots=query.hotList(type=4))

@app.route('/health')
def health():
    return render_template('front/health.html', list=query.newslist(type=5, PC=__ISPC()), hots=query.hotList(type=5))

@app.route('/load_more/<int:type>/<int:offset>')
@app.route('/load_more/<int:offset>/<string:keyword>')
def load_more(offset = 0, keyword = None, type = 1):
    if keyword != None:
        news = query.search(keyword, offset, PC = __ISPC())
    else:
        news = query.newslist(offset, type=type, PC = __ISPC())

    if len(news) == 0:
        return ''

    return render_template('front/newsFactory.html', list = news)


@app.route('/detail/<string:id>')
def detail(id):
    return render_template('front/detail.html', info=query.detail(id), hots=query.hotList())

@app.route('/channel/w/<string:keyword>')
@app.route('/search/<string:keyword>')
def search(keyword):
    if request.path.find('/channel/w') >= 0:
        return redirect(url_for('search', keyword=keyword))

    list = query.search(keyword, PC = __ISPC())
    return render_template('front/search.html', list = list, hots = query.hotList())


@app.route('/capture')
def capture():
    query.capture()
    return '<center><h1>success!!</h1></center>'


@app.route('/test')
@app.route('/test/<string:retry>')
def test(retry):
    return query.test(retry)



def __ISPC():
    header = request.headers
    devices = ("Android", "iPhone", "SymbianOS", "Windows Phone", "iPod")
    flag = True
    print header
    for device in devices:
        if header['User-Agent'].find(device) >= 0:
            flag = False
            break

    return flag


if __name__ == '__main__':
    query.auto_script()
    app.run(debug = True)
