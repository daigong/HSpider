# -*- coding: utf-8 -*-

import time
import threading
import Queue
from website import HenHenluTopicUrlExer, HenHenLuSearchTopicUrl
from thread_pool import ThreadPool
from models import save_topic_and_imgs_to_db

PIC_TYPE = 'yazhou'
START_NUM = 10000
END_NUM = 84449
BASE_URL = 'http://www.toutoulu.com/html/tupian/yazhousetu/%s.html'


def save_url_image_job(web_site_instance):
    try:
        web_site_instance.connect()
        save_topic_and_imgs_to_db(web_site_instance)
    except Exception, e:
        print e


def build_url_job(search_instance, url_task_queue):
    search_instance.connect()
    urls = search_instance.get_topic_urls()
    if len(urls) != 0:
        for url in urls:
            exer = HenHenluTopicUrlExer(url, PIC_TYPE)
            url_task_queue.put((save_url_image_job, (exer,)))


class TopicSearcherThreader(threading.Thread):

    def __init__(self, task_queue):
        threading.Thread.__init__(self)
        self.setName('TopicSearcherThreader')
        self.setDaemon(True)
        self.task_queue = task_queue

    def run(self):
        cur_index = END_NUM
        end_index = cur_index - 1001
        if end_index <= START_NUM:
            end_index = START_NUM - 1
        while True:
            if self.task_queue.qsize() < 1000:
                self.build_task(cur_index, end_index)
                cur_index = cur_index - 1000
                end_index = cur_index - 1001
                if end_index <= START_NUM:
                    end_index = START_NUM - 1
                if cur_index <= START_NUM:
                    break
            time.sleep(20)

    def build_task(self, cur_index, end_index):
        for task_no in range(cur_index, end_index, -1):
            htu = HenHenLuSearchTopicUrl(BASE_URL % str(task_no))
            self.task_queue.put((build_url_job, (htu, self.task_queue)))


def main():

    url_task_queue = Queue.Queue()
    topic_threader = TopicSearcherThreader(url_task_queue)
    topic_threader.start()
    thread_searcher_pool = ThreadPool(20, url_task_queue)
    thread_searcher_pool.start()
    thread_pool = ThreadPool(20, url_task_queue)
    thread_pool.start()

    while True:
        print '#######################################'
        print 'Thread Pool has task count: %s' \
            % str(thread_searcher_pool.current_task_count())
        print '#######################################'
        time.sleep(5)

    topic_threader.join()
    thread_pool.wait_done()
    thread_searcher_pool.wait_done()


if __name__ == '__main__':
    main()
