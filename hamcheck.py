# -*- coding: utf-8 -*-
"""
特定のWebサイトのデータを30秒ごとに取得して
差分を表示する
ハム速専用版:article-body-moreのみ比較

pip install beautifulsoup4
が必要

python3 hamcheck.py <URL>

"""
import os
import sys
import time
import json
import urllib.request
import ssl
import difflib
import pprint
from bs4 import BeautifulSoup
from datetime import datetime


def main() -> None:
    #監視記事のURLをセット
    url = None

    if len(sys.argv) < 2 or 0 != sys.argv[1].find('http'):
        print('usage python3 webdiff.py <URL>')
        return
    url = sys.argv[1]

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    pre_lines = []

    d = difflib.Differ()

    while True:
        now = datetime.now()
        current_sec = now.second
        if 0 == current_sec % 60:
        # if True:
            try:
                with urllib.request.urlopen(url, context=context) as response:
                    body = response.read()
                    status = response.getcode()

                    print('{0:%Y-%m-%d %H:%M:%S}:{1}'.format(now, status))
                    cur_lines = body.decode('utf-8')
                    #cur_lines = cur_lines.splitlines()
                    cur_soup = BeautifulSoup(cur_lines, 'html.parser')
                    #本文記事クラス
                    #cur_innner = cur_soup.select('div.article-body-more')
                    cur_innner = cur_soup.find('div', {'class': 'article-body-more'})
                    if cur_innner is not None:
                        cur_ele = cur_innner.decode_contents(formatter="html")
                        cur_lines = cur_ele.splitlines()
                        # pprint.pprint(cur_lines)
                        # cur_lines = [(s + '\n') for s in cur_lines]
                        # '\n'.join(cur_lines)
                        # pprint.pprint(cur_lines)
                        # return
                        if pre_lines is not None:
                            diff = list(d.compare(pre_lines, cur_lines))
                            for r in diff:
                                if r[0:1] in ['+', '-']:
                                    print(r.strip())
                        # elif cur_lines is not None:
                        #     for r in cur_lines:
                        #         print('+ ' + r.strip())

                        pre_lines = cur_lines
                    

            except urllib.error.URLError as e:
                print(e.reason)
            time.sleep(1)
        time.sleep(0.5)

if __name__ == '__main__':
    main()