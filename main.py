# -*- coding: utf-8 -*-

import time
import Queue
from website import HenHenLuTopicUrlExer, TopicSearcherThreader, \
    build_url_job
from thread_pool import ThreadPool

PIC_TYPE = 'yazhousetu'
BASE_URL = 'http://www.toutoulu.com/html/tupian/yazhousetu/%s.html'
START_NUM = 83761
END_NUM = 84779


def main():

    url_task_queue = Queue.Queue()
    thread_searcher_pool = ThreadPool(200, url_task_queue)
    thread_searcher_pool.start()
    topic_searcher_urls_pool = ThreadPool(50)
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
