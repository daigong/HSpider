# -*- coding: utf-8 -*-

from urllib import urlencode
from models import get_session, PicTopic, PicImg
from thread_pool import ThreadPool
from util.http_utils import HttpAgent

API_URL = 'http://127.0.0.1:8000/api/new/5/'


class Dumper(object):

    def __init__(self, api_url):
        self.http = HttpAgent()
        self.api_url = api_url

    def dump(self, subject, message):
        data = {'message': message, 'subject': subject}
        (reps, context) = self.http.request(self.api_url, 'POST',
                urlencode(data))


def main():
    pool = ThreadPool(20)
    pool.start()
    session = get_session()
    topic_query = session.query(PicTopic).filter(PicTopic.pic_type
            == 'dongmantupian').order_by(PicTopic.id.desc())
    for pic_topic in topic_query:
        pool.add_task(dump_job, pic_topic)
    session.close()

    pool.wait_done()


def dump_job(topic):
    session = get_session()
    subject = topic.title
    message = ''
    imgs_url_query = session.query(PicImg).filter(PicImg.pic_topic_id
            == topic.id).order_by(PicImg.pic_order.asc())
    for img in imgs_url_query:
        message = message + '[img]%s[/img]' % img.url
    subject = subject.encode('utf-8')
    message = message.encode('utf-8')
    dumper = Dumper(API_URL)
    dumper.dump(subject, message)
    session.close()
    print '%s is ok' % subject


main()

# dumper = Dumper()
# message = \
#    ' [img]http://f.hiphotos.baidu.com/album/w%3D1366%3Bcrop%3D0%2C0%2C1366%2C768/sign=4c2a996a622762d0803ea0bc96da3399/79f0f736afc37931ef93a060eac4b74542a911fb.jpg[/img]'
# subject = '题目new1'
# dumper.dump(subject, message)
