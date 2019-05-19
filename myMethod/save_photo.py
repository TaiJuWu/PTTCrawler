import myMethod.methods as m
import requests
import os
import sys
import csv
import time


def save_photo(url ,path):
    # url = 'https://i.imgur.com/GAAF9V1.jpg'
    # path = 'C:/Users/User/Desktop/learn/proj/python/WebCrawler/1.jpg'
    res = m.getRequest(url)
    if res.status_code == requests.codes.ok:
        with open(path ,'wb') as fp:
            for chuck in res:
                fp.write(chuck)
        print(url + '  download success')
    else :
        print('http request error')

def get_img_urls_in_a_page(url):
    res = m.getRequest(url)
    html = m.html_parse(res.text)
    # print(html)
    main_content = html.find(id = 'main-content')
    # print(main_content)
    richcontent = main_content.find_all(class_ = 'richcontent')
    # print(richcontent)
    img_urls =[]
    for img in richcontent:
        try:
            img_url = img.find('a')['href']
            img_urls.append('https:' + img_url +'.jpg')
            # print('https:' + img_url +'.jpg')
        except TypeError as err:
            print(err)
    return img_urls

def download_photo_in_a_article(url ,folder):
    # folder = sys.path[0] +'/Beauty/' + folder
    print(url + 'is download')
    img_urls = get_img_urls_in_a_page(url)
    if not os.path.isdir(folder):
        os.mkdir(folder)
    index = 1
    for url in img_urls:
        save_photo(url ,folder + '/' +str(index) + '.jpg')
        index = index +1


def read_article_url_from_csv(path):
    urls = []
    try:
        with open(path,'r',newline='',encoding='utf8') as fp:
            reader = csv.reader(fp)
            for row in reader:
                if row[1] != 'address':
                    urls.append('https://www.ptt.cc' + row[1])
        return urls
    except FileNotFoundError as err:
        print(err)
        time.sleep(60)
        read_article_url_from_csv(path)
