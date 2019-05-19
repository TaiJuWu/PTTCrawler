import myMethod.methods as m
import time
import threading
import os

def remove_kanbans_csv(kanbans):
    base_path = 'crawlerData/'
    for kanban in kanbans:
        os.remove(base_path + kanban +'.csv')


if __name__ == '__main__':
    # Kanbans =["Gossiping" ,'NBA' ,'Baseball' ,'C_Chat' , 'Boy-Girl' ,'graduate' ,'Grad-ProbAsk','gay' ,'LGBT_SEX' ,'sex' ,'SENIORHIGH' ,'WomenTalk']
    Kanbans =['Baseball']
    key_id = ['q79236' ,'skyHuan' ,'TEPLUN' ,'z952' ,'magic83v','Edison1174']
    threads_search_kanban_index = []
    threads_search_kanban_push_data = []
    start = time.time()
    page_number = 10
    #爬取多個看板的前n頁
    for kanban in Kanbans:
        search_kanban_index = threading.Thread(target = m.search_a_kanbna_multiple_page_index ,args = (kanban ,page_number))
        search_kanban_index.start()
        threads_search_kanban_index.append(search_kanban_index)
        

    #等待上面的程式爬取完成
    for thread in threads_search_kanban_index:
        thread.join()


    #爬取上面程式所擁有的資料，搜尋特定id的推文
    for kanban in Kanbans:
        a_thread_search_kanban_push_data = threading.Thread(target = m.search_kanban_push_data ,args = (kanban ,key_id))
        a_thread_search_kanban_push_data.start()
        threads_search_kanban_push_data.append(a_thread_search_kanban_push_data)
        
    for thread in threads_search_kanban_push_data:
        thread.join()

    print('花了' , time.time() - start ,'s')

    # m.remove_kanbans_csv(Kanbans)



    # 爬取多個看板的第一頁
    # for item in Kanbans:
    #     url = URL.format(item)
    #     url_kanbans.append(url)
    #     index_path = base_path + item +'.csv'
    #     res = getRequest(url)
    #     if res.status_code == requests.codes.ok:
    #         save_kanban_data = get_kanbans_index_data(res)
    #         save_to_csv (index_path ,save_kanban_data)
    #     else:
    #         print('http request error')
    # print(url_kanbans)
        
    # urls =[]
    # urls = get_multiple_page(URL ,10)
    # for url in urls:
    #     res = getRequest(url)
    #     if res.status_code == requests.codes.ok:
    #         save_kanban_data = get_kanbans_index_data(res)
    #         save_to_csv(index_path ,save_kanban_data)
    #     else:
    #         print('http request error')
