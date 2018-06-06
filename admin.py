# -*- coding: utf-8 -*-
"""
    admin
    ~~~~~~
    :copyright: (c) 2018 by Taffy.
"""

from flask import request, redirect, url_for, render_template, Blueprint, make_response, session
from app import query
import time

admin_api = Blueprint('admin_api', __name__)

#定义一个装饰器用于拦截用户登录
def login_require(func):
    def decorator(*args,**kwargs):
        if 'username' in session and request.cookies.get('logintype'):
            return func(*args,**kwargs)
        else:
            return redirect(url_for('admin_api.login'))

    return decorator


@admin_api.route('/login')
def login():
    res = make_response(render_template('admin/login.html'))
    # res.set_cookie('logintype', True, expires=time.time() + 6 * 60 * 24 * 30)
    return res


@admin_api.route('/post')
@login_require
def post():
    return '<center>post</center>'


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





