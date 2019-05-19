import requests
from bs4 import BeautifulSoup
import os
import csv
import re
from urllib.parse import urlparse
import time


def getRequest(url):
    header ={
       ' accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
    }
    return requests.get(url ,header ,cookies={"over18" :"1"})

def html_parse(text):
    return BeautifulSoup(text ,'lxml')

def save_to_csv(file ,text):
    try:
        # if os.path.isfile(file):
        #     os.remove(file)
        with open(file ,'a+' ,encoding='utf8' ,newline='') as fp:
            writer = csv.writer(fp)
            writer.writerow(['title' , 'address' ,'author' ,'date'])
            # print(text)
            for row in text:
                # print(row)
                writer.writerow(row)
    except PermissionError as err:
        print('wait some time to read' ,err)
        time.sleep(60)
        save_to_csv(file ,text)
    


def save_person_push_to_csv(file ,text):
    try:
        with open(file ,'a+' ,encoding='utf8' ,newline='') as fp:
            writer = csv.writer(fp)
            writer.writerow(text)
    except PermissionError as err:
        print('wait some time to read' ,err)
        time.sleep(60)
        save_person_push_to_csv(file ,text)

#read data store in csv
def read_from_csv(kanban):
    urls = []
    try:
        with open('crawlerData/' + kanban +'.csv','r',newline='',encoding='utf8') as fp:
            reader = csv.reader(fp)
            for row in reader:
                if row[1] != 'address':
                    urls.append(row[1])
        return urls
    except FileNotFoundError as err:
        print(err)
        time.sleep(60)
        read_from_csv(kanban)
    

#get the data about key_id
def get_push_data(res, key_id):
    store_path = 'crawlerData\destination_person'
    html = html_parse(res.text)
    title = html.find('title').text
    html_push_mans = html.find_all(class_ = 'push-userid')
    html_push_content =html.find_all(class_='push-content')
    html_push_ipdatetime =html.find_all(class_='push-ipdatetime')
    push_data = []

    for man in html_push_mans:
        data = []
        data.append(man.text)
        data.append(html_push_content.pop(0).text)
        data.append(html_push_ipdatetime.pop(0).text.replace('\n',""))
        push_data.append(data)

    for data in push_data:
        if data[0] in key_id:
            name = data[0]
            data.insert(0 ,title)
            if not os.path.isdir(store_path):
                os.mkdir(store_path)
            save_person_push_to_csv(store_path + '/' + name +'.csv' , data)


#we can get the multiple page for a kanban
def get_multiple_page(url ,pag_number):
    url_base =urlparse(url).scheme + '://' + urlparse(url).netloc
    # print(urlparse(url))
    url_pages = []
    res = getRequest(url)
    html = html_parse(res.text)
    page = html.find(text='‹ 上頁')
    page_now = page.parent['href']
    # print('page : ',page_now)
    index_position = re.search('index' , page_now).span()[-1]
    dot_pisition = re.search('\.',page_now).span()[0]
    page_index = page_now[index_position:dot_pisition]
    # print(page_index)
    url_pages.append(url)
    for i in range(pag_number-1):
        if int(page_index)-i < 1:
            break
        url_pages.append(url_base + page_now.replace(page_index ,str(int(page_index)-i)))
    # print(url_pages)
    return url_pages

#parse the data of kanban
def get_kanbans_index_data(res):
    #DELETE = BeautifulSoup("<a href='delete'> 本文已被刪除 </a>" ,'lxml').a
    save_data =[]
    html = html_parse(res.text)
    titles = html.find_all(class_ = 'title')
    authors = html.find_all(class_='author')
    dates = html.find_all(class_='date')
    for title in titles:
        save =[]
        if title.a != None:
            tag_a= title.a #or DELETE
            # print(tag_a)
            # if not isinstance(tag_a ,'NoneType'): 沒用
            save.append(tag_a.text)
            save.append(tag_a['href'])
            save.append(authors.pop(0).text)
            save.append(dates.pop(0).text)
            save_data.append(save)
    return save_data

#main function
def search_a_kanbna_multiple_page_index(Kanban ,page_number):
    save_kanban_data= []
    url_kanbans =[]
    URL = 'https://www.ptt.cc/bbs/{0}/index.html'
    base_path = 'crawlerData/'
    print('正在爬取看版資料:' + Kanban)
    url_kanban = URL.format(Kanban)
    url_kanbans.append(url_kanban)
    index_path = base_path + Kanban +'.csv'
    urls =[]
    urls = get_multiple_page(url_kanban ,page_number)
    for url in urls:
        res = getRequest(url)
        if res.status_code == requests.codes.ok:
            print('爬取看板' + url +'的index')
            save_kanban_data = get_kanbans_index_data(res)
            save_to_csv(index_path ,save_kanban_data)
        else:
            print(url + '  http request error')


def search_kanban_push_data(kanban , key_id):
    url_domain = 'https://www.ptt.cc'
    print('正在爬取' + kanban + '的推文資料')
    urls = read_from_csv(kanban)
    for url in urls:
        URL = url_domain + url
        res = getRequest(URL)
        if res.status_code == requests.codes.ok:
            get_push_data(res ,key_id)
            print('爬取' + url +'的推文資料')
        else:
            print(url + '  http request error')


def remove_kanbans_csv(kanbans):
    base_path = 'crawlerData/'
    for kanban in kanbans:
        os.remove(base_path + kanban +'.csv')
