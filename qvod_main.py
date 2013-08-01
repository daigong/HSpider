# -*- coding: utf-8 -*-

import httplib2
from pyquery import PyQuery as pq
from urllib import unquote


class HenHenLuQvodInfo(object):

    """QvodInfo"""

    def __init__(self, qvod_id):
        self.http = httplib2.Http(timeout=10)
        self.qvod_id = qvod_id
        self.imgs = []

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
        print unquote(url)


def main():
    info = HenHenLuQvodInfo(27038)
    info.get_imgs()
    info.get_qvod_address()


main()