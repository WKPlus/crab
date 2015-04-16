#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""
html tag checker for scod.

@author: qifa.zhao@dianping.com
@license: Copyright (c) 2013 Dianping.com, Inc. All Rights Reserved

"""

import os
import sys
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "../")))
from lib.html_parser import HTMLTagParser
from lib.log import GLog
from lib.reader import HTMLReader
from selenium.common.exceptions import TimeoutException


class HTMLTagChecker(object):
    def __init__(self):
        self.html_reader = HTMLReader()
        self.err_msg = ''

    def check(self, url):
        url, content = self.html_reader.read_content(url)
        parser = HTMLTagParser()
        parser.feed(content)
        unmatch_tags = parser.close()
        for t in unmatch_tags:
            self.err_msg += 'Broken %s tag[%s] in pos[%s,%s]\n'\
               % ('start' if t.start else 'end', t.name, t.pos[0], t.pos[1]) 
            GLog.warning("Broken %s tag[%s] in pos[%s,%s] in url: %s",
                "start" if t.start else "end", t.name, t.pos[0], t.pos[1], url)
        if len(unmatch_tags) != 0:
            return (1, self.err_msg)
        else:
            return (0, '')


class ContentChecker(object):
    def __init__(self, wait_condition, cookies=None, localStorage=None):
        self.wait_condition = wait_condition
        self.cookies = cookies
        self.localStorage = localStorage
        self.html_reader = HTMLReader()

    def check(self, url):
        try:
            content = self.html_reader.read_content_wait(url, self.wait_condition,
                                              cookies=self.cookies,
                                              localStorage=self.localStorage) 
            return (0, '')
        except TimeoutException:
            return (1, 'Page access Timeout!\n')


def test_HTMLTagChecker():
    checker = HTMLTagChecker()
    url_list = []
    #url_list.append("www.baidu.com")
    #url_list.append("www.dianping.com/citylist")
    url_list.append('http://192.168.5.148/pray.html')
    for url in url_list:
        ret = checker.check(url)
        print ret


def test():
    test_HTMLTagChecker()


if __name__ == "__main__":
    test()
