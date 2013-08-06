# -*- coding: utf-8 -*-

from httplib2 import Http


class HttpAgent(object):

    default_header = {
        'User-Agent': ' Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.79 Safari/537.1',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Accept-Encoding': 'gzip,deflate,sdch',
        }

    def __init__(self, *args, **kwargs):
        self.http = Http(*args, **kwargs)

    def request(self, *args, **kwargs):
        headers = kwargs.pop('headers', dict())
        headers.update(HttpAgent.default_header)
        kwargs['headers'] = headers
        return self.http.request(*args, **kwargs)
