# -*- coding: utf-8 -*-

from pyquery import PyQuery as pq
from thread_pool import ThreadPool
from models import VideoTopic, get_session
from util.http_utils import HttpAgent


class HenHenVideoPage(object):

    """VideoPage """

    def __init__(self, url, video_type):
        self.http = HttpAgent(timeout=10)
        self.url = url
        self.video_type = video_type

    def get_video_info(self):
        title_list = list()
        video_id_list = list()
        (reps, content) = self.http.request(self.url)
        d = pq(content)
        for tag_box in d('.list-pianyuan-box'):
            tag_url_a = pq(tag_box)('.list-pianyuan-box-l a')
            pq_a = pq(tag_url_a)
            url_id_text = pq_a.attr('href')
            title_list.append(pq_a.attr('title'))
            henhenluid = url_id_text[url_id_text.rfind('/')
                + 1:url_id_text.find('.')]
            video_id_list.append(henhenluid)

        return (title_list, video_id_list)

    def save_to_db(self):
        (title_list, video_id_list) = self.get_video_info()
        session = get_session()
        try:
            for index in range(0, len(video_id_list)):
                topic = VideoTopic(title_list[index], 'henhenlu',
                                   self.video_type,
                                   video_id_list[index])

                session.add(topic)
                session.commit()
                print video_id_list[index] + ' is ok'
        finally:
            session.close()


def check_page_max():
    http = HttpAgent()
    base_url = 'http://www.toutoulu.com/vodlist/7_%s.html'
    for i in range(11, 2000, 1):
        (reps, content) = http.request(base_url % str(i))
        if reps['status'] == '404':
            print '%d is 404' % i
            break
        else:
            print '%d is ok' % i


def thread_pool_job(url, video_type):
    page = HenHenVideoPage(url, video_type)
    page.save_to_db()


page_info = {
    '1': 567,
    '2': 80,
    '3': 175,
    '4': 27,
    '5': 33,
    '6': 172,
    '7': 20,
    }


def main():
    thread_pool = ThreadPool(50)
    thread_pool.start()
    video_type = '7'
    base_url = 'http://www.toutoulu.com/vodlist/%s_%s.html'

    # init task

    for page_num in range(1, page_info[video_type] + 1):
        url = base_url % (video_type, page_num)
        print 'add task %s' % url
        thread_pool.add_task(thread_pool_job, url, video_type)

    thread_pool.wait_done()


main()

# 1_567
# 2_80
# 3_175
# 4_27
# 5_33
# 6_172
# 7_20

#    page = HenHenVideoPage('http://www.toutoulu.com/vodlist/1_1.html')
#    print page.get_video_id()

