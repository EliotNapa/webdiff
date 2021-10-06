# -*- coding: utf-8 -*-
"""
特定のWebサイトのデータを30秒ごとに取得して
差分を表示する

python3 webdiff.py <URL>

"""
import os
import sys
import time
import json
import urllib.request
import ssl
import difflib
import pprint
from datetime import datetime


def main() -> None:
    #監視記事のURLをセット
    url = None

    if len(sys.argv) < 2 or 0 != sys.argv[1].find('http'):
        print('usage python3 hamuget.py <URL>')
        return
    url = sys.argv[1]

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    pre_lines = None

    d = difflib.Differ()

    while True:
        now = datetime.now()
        current_sec = now.second
        if 0 == current_sec % 30:
            try:
                with urllib.request.urlopen(url, context=context) as response:
                    body = response.read()
                    status = response.getcode()

                    print('{0}:{1}'.format(now, status))
                    cur_lines = body.decode('utf-8')
                    cur_lines = cur_lines.splitlines()

                    if pre_lines is not None:
                        diff = list(d.compare(cur_lines, pre_lines))
                        for r in diff:
                            if r[0:1] in ['+', '-']:
                                print(r.strip())

                    pre_lines = cur_lines
                    

            except urllib.error.URLError as e:
                print(e.reason)
        time.sleep(1)

if __name__ == '__main__':
    main()