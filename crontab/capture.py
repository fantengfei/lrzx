# -*- coding: utf-8 -*-

import requests
import time

if __name__ == '__main__':
    re = requests.get('https://www.somenews.cn/capture')
    localtime = time.asctime(time.localtime(time.time()))
    print localtime + ': '
    print re.content