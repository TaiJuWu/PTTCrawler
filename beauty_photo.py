import myMethod.methods as m
import myMethod.save_photo as ph
import requests
import sys
import os
import threading
import time


if __name__ == '__main__':
    start_time = time.time()
    page_number = 10
    Kabnan = 'Beauty'
    save_kanban_data= []
    URL = 'https://www.ptt.cc/bbs/Beauty/index.html'
    folder = os.getcwd() + '/Beauty'
    # print(sys.path[0])
    if not os.path.isdir(folder):
        os.mkdir(folder)
        
    index_path = folder + '/index.csv'
    page_urls = m.get_multiple_page(URL ,page_number)
    # print(page_urls)
    if os.path.isfile(index_path):
        os.remove(index_path)

    for url in page_urls:
        res = m.getRequest(url)
        if res.status_code == requests.codes.ok:
            print('爬取看板 ' + url +' 的index')
            save_kanban_data = m.get_kanbans_index_data(res)
            # print(save_kanban_data)
            m.save_to_csv(index_path ,save_kanban_data)
            # print(save_kanban_data)
        else:
            print(url + '  http request error')
    
    article_urls = ph.read_article_url_from_csv(index_path)
    # print(article_urls)
    index = 1
    threads =[]
    for url in article_urls:
        thread = threading.Thread(target = ph.download_photo_in_a_article ,args=(url ,folder + '/' + str(index)))
        thread.start()
        threads.append(thread)
        # ph.download_photo_in_a_article(url ,folder + '/' + str(index))
        index = index +1
    
    for thread in threads:
        thread.join()
    end_time = time.time()
    run_time = end_time - start_time
    sec = run_time % 60
    min = run_time // 60
    print('共花了' + min + 'min' + sec +'s')
    # os.remove(index_path)




