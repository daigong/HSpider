# -*- coding: utf-8 -*-

import time
import Queue
from website import HenHenLuTopicUrlExer, TopicSearcherThreader
from thread_pool import ThreadPool
from models import save_topic_and_imgs_to_db

PIC_TYPE = 'yazhousetu'
BASE_URL = 'http://www.toutoulu.com/html/tupian/yazhousetu/%s.html'
START_NUM = 83761
END_NUM = 84779


def save_url_image_job(web_site_instance):
    try:
        web_site_instance.connect()
        save_topic_and_imgs_to_db(web_site_instance)
    except Exception, e:
        print e


def build_url_job(search_instance, topic_img_searcher_pool,
                  website_class):
    search_instance.connect()
    urls = search_instance.get_topic_urls()
    if len(urls) != 0:
        for url in urls:
            exer = website_class(url, PIC_TYPE)
            topic_img_searcher_pool.add_task(save_url_image_job, exer)


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
