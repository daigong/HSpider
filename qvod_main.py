# -*- coding: utf-8 -*-

# proxy :python-socksipy  (socks)

# import socks
# import httplib2

from pyquery import PyQuery as pq
from urllib import unquote
from util.http_utils import HttpAgent
from models import VideoImg, Video, VideoTopic, get_session
from thread_pool import ThreadPool


# h = httplib2.Http(proxy_info = httplib2.ProxyInfo(socks.PROXY_TYPE_HTTP, 'localhost', 8000))

class HenHenLuQvodInfo(object):

    """QvodInfo"""

#        self.http = \
#            httplib2.Http(proxy_info=httplib2.ProxyInfo(socks.PROXY_TYPE_HTTP,
#                          '61.51.111.61', 8443))

    def __init__(self, qvod_id):

        # self.http = \
        #    HttpAgent(proxy_info=httplib2.ProxyInfo(socks.PROXY_TYPE_HTTP,
        #              '218.245.6.4', 99))

        self.http = HttpAgent()
        self.qvod_id = qvod_id
        self.imgs = []

    def test(self):
        (resp, content) = self.http.request('http://www.toutoulu.com')
        print resp

    def get_imgs(self):
        (resp, content) = \
            self.http.request('http://www.toutoulu.com/vod/%s.html'
                              % self.qvod_id)
        q = pq(content)
        imgs_list = q('.nr-box .vpl img')
        for img in imgs_list:
            self.imgs.append(pq(img).attr('src'))
        self.qvod_src = q('.vmain .vpl a').attr('href')

    def get_qvod_address(self):
        (resp, content) = self.http.request(self.qvod_src)
        q = pq(content)
        address = q('.playbox2-c script').text()
        index_begin = address.find('var url_list="')
        address = address[index_begin:]
        index_begin = address.find('qvod')
        index_end = address.rfind('%7C')
        url = address[index_begin:index_end + 3]
        self.qvod_address = unquote(url).decode('utf-8')

    def save_to_db(self):
        session = get_session()
        try:
            video_topic = \
                session.query(VideoTopic).filter(VideoTopic.henhen_id
                    == self.qvod_id).first()
            index_order = 0
            for img in self.imgs:
                video_img = VideoImg()
                video_img.pic_order = index_order
                video_img.url = img
                video_img.video_topic_id = video_topic.id
                index_order = index_order + 1
                session.add(video_img)
            video = Video()
            video.video_topic_id = video_topic.id
            video.url = self.qvod_address
            session.add(video)
            session.commit()
        finally:
            session.close()

    def do_all_job(self):
        self.get_imgs()
        self.get_qvod_address()
        self.save_to_db()
        print 'qvod : %s is ok' % self.qvod_address


def job(qvod_id):
    info = HenHenLuQvodInfo(qvod_id)
    info.do_all_job()


def main():
    info = HenHenLuQvodInfo(14)
    info.do_all_job()


def main1():
    thread_pool = ThreadPool(20)
    thread_pool.start()
    session = get_session()
    topic_query = \
        session.query(VideoTopic).filter(VideoTopic.video_type == 1)
    for topic in topic_query:
        thread_pool.add_task(job, topic.henhen_id)
    session.close()
    thread_pool.wait_done()


#    info.get_imgs()
#    info.get_qvod_address()

main()
