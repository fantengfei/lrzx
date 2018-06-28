#-*- coding:utf-8 -*-
"""
    common
    ~~~~~~
    :copyright: (c) 2018 by Taffy.
"""

import re

def md5(str):
    import hashlib
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()


def analysisImgs(html):
    # img标签的正则式
    replace_pattern = r'<[img|IMG].*?/>'
    # img_url的正则式
    img_url_pattern = r'.+?src="(\S+)"'
    img_url_list = []
    # 找到所有的img标签
    need_replace_list = re.findall(replace_pattern, html)
    for tag in need_replace_list:
        # 找到所有的img_url
        img_url_list.append(re.findall(img_url_pattern, tag)[0])

    return img_url_list