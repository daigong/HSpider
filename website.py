# -*- coding: utf-8 -*-

import httplib2
from pyquery import PyQuery as pq


class HenHenLuSearchTopicUrl(object):

    def __init__(self, url):
        self.url = url
        self.topic_urls = []
        self.http = httplib2.Http(timeout=10)

    def connect(self):
        (reps, content) = self.http.request(self.url)
        if reps['status'] != '404':
            self.topic_urls.append(self.url)
            print "URL: %s is ok" % self.url

    def get_topic_urls(self):
        return self.topic_urls


class HenHenluTopicUrlExer(object):

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


