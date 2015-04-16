# -*- coding:utf-8 -*-
"""
base case definition.

@author: qifa.zhao@dianping.com  xin.he@dianping.com
@license: Copyright (c) 2014 Dianping.com, Inc. All Rights Reserved

"""

import time
from lib.log import GLog
from lib.page import Page, Result
from lib.extractor.href_extractor import Extractor
from collections import deque


class TestCase(object):
    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:25.0) "
        "Gecko/20100101 Firefox/25.0"
    )
    def __new__(cls):
        obj = object.__new__(cls)
        #这里初始化一些在_init之前可能使用到的成员
        obj.urls = []
        obj.extractors = []
        obj.checkers = []
        return obj

    def add_url(self, url, depth=0):
        if isinstance(url, str):
            self.urls.append((url, depth))
        elif isinstance(url, (tuple, list)):
            self.urls.extend(((u, depth) for u in url))
        else:
            raise Exception('wrong param for add_url')

    def add_checker(self, checker):
        self.checkers.append(checker)

    def add_link_extractor(self, ex):
        self.extractors.append(ex)

    def page_ready(self, page):
        self.check(page)

    def connection_close(self):
        #一旦一个connect close了，其对应的链接可以认为关闭了
        #如果此时有hold住的request，可以打开一个
        if self.concurrency:
            self.connection_num -= 1
            if self.hold_requests:
                u, depth, ua, parent = self.hold_requests.popleft()
                self._add_page(u, depth, ua, parent)

    def is_white_url(self, url):
        #判断一个url是不是位于白名单中，用于忽略一些已知问题
        return False

    def check(self, page):
        GLog.debug("Checking url: %s", page.url)
        for checker in self.checkers:
            r, msg = checker.check(page)
            if not r:
                self.result.append(Result(page, msg))

    def extract_links(self, page):
        url, content = page.url, page.page_source
        sub_links = set()
        for ex in self.extractors:
            links = ex.extract(url, content)
            sub_links = sub_links.union(links)
        for u in sub_links:
            self._add_page(u, page.depth - 1, page.ua, url)

    def _add_page(self, u, depth=0, ua=USER_AGENT, parent=None):
        if self.concurrency:
            #限制并发
            if self.connection_num < self.concurrency:
                self.connection_num += 1
                Page(self, u, depth, ua, parent)
            else:
                self.hold_requests.append((u, depth, ua, parent))
        else:
            #不限制并发
            Page(self, u, depth, ua, parent)

    def need_page_source(self):
        #TODO: 优化效率，如果checkers都不需要使用page source，返回False
        return True

    def run(self, report_handler, concurrency=0):
        #处理一些默认操作，比如添加最基本的link_extractor
        if not self.extractors:
            self.extractors.append(Extractor())
        self.report_handler  = report_handler
        self.concurrency = concurrency
        self.connection_num = 0
        self.hold_requests = deque()
        self.result = []
        #生成Page对象
        for u, d in self.urls:
            self._add_page(u, d)

    def finish(self):
        self.report_handler(self)
