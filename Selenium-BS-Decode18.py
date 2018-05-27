#!/usr/bin/env python
# -*- coding: utf-8 -*-

# de:code18のセッション一覧を取得する
#############################################

import bs4
import codecs
import datetime
import os
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# import urllib.request


# const
url = 'https://www.microsoft.com/ja-jp/events/decode/2018/sessions.aspx'

cd = os.path.expanduser(
    '~\\OneDrive\\ドキュメント\\works\\Python\\Sele\\Sele-Decode18')
# cd = os.path.dirname(os.path.abspath(__file__))


os.chdir(cd)
print(os.getcwd())


def get_source(url):
    '''
    URLを指定してHTMLソースを取得
    動的に生成されたソースを取るためにSeleniumを使用
    '''
    global fox
    fox.get(url)
    WebDriverWait(fox, 30).until(
        EC.presence_of_element_located((By.ID, 'SP62')))
    html_post = fox.page_source
    return(html_post)


# Seleniumを起動
# fox = webdriver.Firefox()
binary = FirefoxBinary('C:\\Program Files\\Mozilla Firefox\\firefox.exe')
fox = webdriver.Firefox(firefox_binary=binary)

fox.set_window_size(1280, 240)

# パース
soup = bs4.BeautifulSoup(get_source(url), "lxml")
html_post_title = soup.title.string
print(html_post_title)

div_box_session = soup.find('div', class_='box-session')
div_sort = div_box_session.find('div', class_='sort')

sessions = div_sort.find_all('section', id=re.compile('[A-Z]{2}[0-9]{2}'))

# タグ、ジャンル、タイトルを取得して、リストに追加
list_csv = []

for i, session in enumerate(sessions):
    print(str(int((100*i)/len(sessions)))+'%')  # 進捗状況

    genre = session.select_one('h4.item-session__type').text
    tag = session.find('h4', class_='item-session__type').find('span').text
    time = session.find(
        'p', class_='item-session__time').text.replace(':', '').replace(' – ', '-')
    title = session.find('h3', class_='item-session__headline').text

    genre = genre.replace(tag, '')

    content = tag + "," + genre + " " + time + " " + tag + " " + title
    content = re.sub(r'[\\/:*?"<>\|.]', '_', content)
    content = content.replace('\u3000', '_').replace('?', '_')

    print(content)
    list_csv.append(content)

# 後片付け
fox.close()
try:
    fox.quit()
except:
    pass


# リストを整形
list_csv.sort()


# 出力
now = datetime.datetime.now()
listfile_name = 'list_{0:%Y%m%d%H%M%S}.txt'.format(now)
listfile_path = os.path.join(cd, listfile_name)
with codecs.open(listfile_path, 'a', 'utf-8') as file:
    file.write("\n".join(list_csv))


# Copyright (c) 2018 YA-androidapp(https://github.com/YA-androidapp) All rights reserved.
