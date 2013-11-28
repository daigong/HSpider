# -*- coding: utf-8 -*-

import urllib2
import random
import time
import contextlib

# demo http://minchoi.jp/api/auth/sendauthmail/gretaky@hotmail.co.jp/19800508/

URL_TEMPLATE = 'http://minchoi.jp/api/auth/sendauthmail/%s/%s/'

FILE_NAME = '/home/daigong/git/HSpider/mail.txt'


def ramdon_bir_date():
    year = random.randint(1980, 1992)
    mouth = random.randint(1, 9)
    day = random.randint(10, 28)
    return '%d0%d%d' % (year, mouth, day)


def job(mail, bir_date):
    print URL_TEMPLATE % (mail,bir_date)
    with contextlib.closing(urllib2.urlopen(URL_TEMPLATE % (mail,
                            bir_date))):
        print ' %s,%s is ok' % (mail, bir_date)
        time.sleep(1)


def main():
    file = open(FILE_NAME, 'r')
    lines = file.readlines()
    for mail_and_password in lines:

        lines_info = mail_and_password.split(',')
        if len(lines_info) != 2:
            print 'Wrong Mail and Password! %s' % str(lines_info)
        else:
            mail = lines_info[0]
            job(mail, ramdon_bir_date())


main()
