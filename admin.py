# -*- coding: utf-8 -*-
"""
    admin
    ~~~~~~
    :copyright: (c) 2018 by Taffy.
"""

from flask import request, redirect, url_for, render_template, Blueprint, make_response, session
from app import adminQuery
import time

admin_api = Blueprint('admin_api', __name__)


@admin_api.before_request
def before_request():
    if request.path == '/login':
        return None

    if 'username' not in session:
        return redirect(url_for('admin_api.login'))



@admin_api.route('/login', methods=['POST', 'GET'])
def login():
    ck = request.cookies.get('username')
    if ck:
        session['username'] = ck
        return redirect(url_for('admin_api.post'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if adminQuery.verify_user(username, password):
            session['username'] = username
            res = make_response('success')
            res.set_cookie('username', username, expires=time.time() + 6 * 60 * 24 * 30)
            return res
        else:
            return '账号或密码错误！'

    return render_template('admin/login.html')


@admin_api.route('/post')
def post():
    return render_template('admin/post.html')


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





