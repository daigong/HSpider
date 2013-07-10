# -*- coding: utf-8 -*-

import httplib2
import threading
import time
from pyquery import PyQuery as pq
from models import save_topic_and_imgs_to_db


class HenHenLuSearchTopicUrl(object):

    def __init__(self, url):
        self.url = url
        self.topic_urls = []
        self.http = httplib2.Http(timeout=10)

    def connect(self):
        (reps, content) = self.http.request(self.url)
        if reps['status'] != '404':
            self.topic_urls.append(self.url)
            print 'URL: %s is ok' % self.url

    def get_topic_urls(self):
        return self.topic_urls


class HenHenLuTopicUrlExer(object):

    def __init__(self, url, pic_type):
        self.url = url
        self.pic_type = pic_type
        self.http = httplib2.Http(timeout=10)

    def connect(self):
        (reps, content) = self.http.request(self.url)
        if reps['status'] != '404':
            self.d = pq(content)

    def get_site_inner_id(self):
        last_dot = self.url.rfind('.')
        last_gang = self.url.rfind('/')
        return self.url[last_gang + 1:last_dot]

    def get_title(self):
        title = self.d('#contain .index_box h2').text()
        if title is not None:
            title = title.strip()
        return title

    def get_image_url_list(self):
        d_imgs_list = self.d('#contain .n_bd img')
        imgs_list = []
        for img in d_imgs_list:
            imgs_list.append(pq(img).attr('src'))
        return imgs_list

    def get_website_type(self):
        return 'henhenlu'

    def get_pic_type(self):
        return self.pic_type

    def is_available(self):
        title = self.get_title()

        # 检查题目是否是NULL或者是空串

        if title is None or title.strip() is '':
            return False

        imgs_list = self.get_image_url_list()

        # 只判断第一张图片是否可用

        if len(imgs_list) > 0:
            try:
                (resp, context) = self.http.request(imgs_list[0])
                if resp['status'] == '200':
                    return True
            except Exception:
                return False
        return False


class TopicSearcherThreader(threading.Thread):

    def __init__(
        self,
        thread_searcher_pool,
        topic_img_searcher_pool,
        job_function,
        website_class,
        base_url,
        start_num,
        end_num,
        pic_type,
        ):

        threading.Thread.__init__(self)
        self.setName('TopicSearcherThreader')
        self.setDaemon(True)
        self.thread_searcher_pool = thread_searcher_pool
        self.topic_img_searcher_pool = topic_img_searcher_pool
        self.website_class = website_class
        self.job_function = job_function
        self.cur_index = None
        self.end_index = None
        self.base_url = base_url
        self.start_num = start_num
        self.end_num = end_num
        self.pic_type = pic_type

    def run(self):
        while True:
            if self.thread_searcher_pool.current_task_count() < 1000:
                print '########################################'
                print 'now task is %s , add 1000 task' \
                    % self.thread_searcher_pool.current_task_count()
                print '########################################'
                if self.move_next_index():
                    break

                self.build_task()

            time.sleep(20)

    def move_next_index(self):

        if self.end_index == self.start_num - 1:
            return True

        if self.cur_index is None and self.end_index is None:
            self.cur_index = self.end_num
            self.end_index = self.cur_index - 1001
            if self.end_index <= self.start_num:
                self.end_index = self.start_num - 1
        else:
            self.cur_index = self.cur_index - 1000
            self.end_index = self.cur_index - 1001
            if self.end_index <= self.start_num:
                self.end_index = self.start_num - 1
        return False

    def build_task(self):
        for task_no in range(self.cur_index, self.end_index, -1):
            htu = HenHenLuSearchTopicUrl(self.base_url % str(task_no))
            self.thread_searcher_pool.add_task(self.job_function, htu,
                    self.topic_img_searcher_pool, self.website_class,
                    self.pic_type)


def save_url_image_job(web_site_instance):
    try:
        web_site_instance.connect()
        save_topic_and_imgs_to_db(web_site_instance)
    except Exception, e:
        print e


def build_url_job(
    search_instance,
    topic_img_searcher_pool,
    website_class,
    pic_type,
    ):

    search_instance.connect()
    urls = search_instance.get_topic_urls()
    if len(urls) != 0:
        for url in urls:
            exer = website_class(url, pic_type)
            topic_img_searcher_pool.add_task(save_url_image_job, exer)


