# -*- coding: utf-8 -*-

import time
import Queue
from website import HenHenLuTopicUrlExer, TopicSearcherThreader, \
    build_url_job
from thread_pool import ThreadPool

# 亚洲
# PIC_TYPE = 'yazhousetu'
# BASE_URL = 'http://www.toutoulu.com/html/tupian/yazhousetu/%s.html'
# START_NUM = 10000
# END_NUM = 84779

# 欧美
# PIC_TYPE = 'oumeisetu'
# BASE_URL = 'http://www.toutoulu.com/html/tupian/oumeisetu/%s.html'
# START_NUM = 10000
# END_NUM = 84876

# 清纯
# PIC_TYPE = 'qingchunweimei'
# BASE_URL = 'http://www.toutoulu.com/html/tupian/qingchunweimei/%s.html'
# START_NUM = 10000
# END_NUM = 84885

PIC_TYPE = 'toupaizipai'
BASE_URL = 'http://www.toutoulu.com/html/tupian/toupaizipai/%s.html'
START_NUM = 10000
END_NUM = 84949


# 动漫
# PIC_TYPE = 'dongmantupian'
# BASE_URL = 'http://www.toutoulu.com/html/tupian/dongmantupian/%s.html'
# START_NUM = 10000
# END_NUM = 84032

# 套图 TODO
# http://www.toutoulu.com/html/tupian/chengrentaotu/2013-07-11/84951.html

def main():

    url_task_queue = Queue.Queue()
    thread_searcher_pool = ThreadPool(500, url_task_queue)
    thread_searcher_pool.start()
    topic_searcher_urls_pool = ThreadPool(200)
    topic_searcher_urls_pool.start()
    topic_threader = TopicSearcherThreader(
        thread_searcher_pool,
        topic_searcher_urls_pool,
        build_url_job,
        HenHenLuTopicUrlExer,
        BASE_URL,
        START_NUM,
        END_NUM,
        PIC_TYPE,
        )
    topic_threader.start()

    while True:
        print '#######################################'
        print 'URL has task count: %s' \
            % str(thread_searcher_pool.current_task_count())
        print '#######################################'
        print '#######################################'
        print 'TOPIC has task count: %s' \
            % str(topic_searcher_urls_pool.current_task_count())
        print '#######################################'

        time.sleep(5)

    topic_threader.join()
    topic_searcher_urls_pool.wait_done()
    thread_searcher_pool.wait_done()


if __name__ == '__main__':
    main()
