"""
example04.py - 单线程版本爬虫
"""
import os

import requests


def download_picture(url):
    filename = url[url.rfind('/') + 1:]
    resp = requests.get(url)
    if resp.status_code == 200:
        with open(f'images/beauty/{filename}', 'wb') as file:
            file.write(resp.content)


def main():
    if not os.path.exists('images/beauty'):
        os.makedirs('images/beauty')
    for page in range(3):
        resp = requests.get(f'https://image.so.com/zjl?ch=beauty&sn={page * 30}')
        if resp.status_code == 200:
            pic_dict_list = resp.json()['list']
            for pic_dict in pic_dict_list:
                download_picture(pic_dict['qhimg_url'])

if __name__ == '__main__':
    main()