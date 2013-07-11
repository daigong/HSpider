# -*- coding: utf-8 -*-

import httplib2
from urllib import urlencode

http = httplib2.Http()
data = {'daigong': '代公'}
(reps, context) = http.request('http://127.0.0.1:8000/api/new/1/',
                               'POST', urlencode(data))

print context
