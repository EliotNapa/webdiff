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


def main():
    #監視記事のURLをセット
    url = None

    if len(sys.argv) < 2 or 0 != sys.argv[1].find('http'):
        print('usage python3 hamuget.py <URL>')
        return
    url = sys.argv[1]

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    pre_buff = None
    pre_lines = None

    d = difflib.Differ()

    while True:
        now = datetime.now()
        current_sec = now.second
        if 0 == current_sec % 30:
            try:
                with urllib.request.urlopen(url, context=context) as response:
                    body = response.read()
                    headers = response.getheaders()
                    status = response.getcode()

                    folder = '{0:%Y%m%m%H%M%S}'.format(now)
                    if not os.path.exists(folder):
                        os.makedirs(folder, exist_ok = True)

                    print('{0}:{1}'.format(now, status))
                    cur_lines = body.decode('utf-8')

                    diff_file = folder + '\diff.txt'
                    if pre_lines is not None:
                        diff = difflib.ndiff(cur_lines, pre_lines)
                        with open(diff_file, mode='w', encoding="utf-8") as fw:
                            for r in diff:
                                if r[0:1] in ['+', '-']:
                                    print(r.strip())
                                    fw.write(r)

                    pre_lines = cur_lines
                    

            except urllib.error.URLError as e:
                print(e.reason)
        time.sleep(1)

if __name__ == '__main__':
    main()