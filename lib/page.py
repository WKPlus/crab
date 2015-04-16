# -*- coding:utf-8 -*-

"""
object definition of page

@author: qifa.zhao@dianping.com
@license: Copyright (c) 2015 Dianping.com, Inc. All Rights Reserved

"""

from lib.utils import fill_url, convert_chinese
from twisted.web.http_headers import Headers
from twisted.web.client import Agent, RedirectAgent, readBody
from twisted.internet import reactor
from twisted.internet.tcp import Client
from twisted.internet.defer import setDebugging
setDebugging(True)



class Page(object):
    __slots__ = ['parent', 'url', 'ua', 'depth',
                 'status', 'page_source', 'test_case']
    _agent = RedirectAgent(Agent(reactor))
    NUM = 0

    def __init__(self, test_case, url, depth, ua, parent):
        self.test_case = test_case
        self.url = fill_url(convert_chinese(url))
        self.parent = parent
        self.depth = depth
        self.ua = ua
        self.status = None
        self.page_source = None

        Page.NUM += 1
        d = self._agent.request(
            'GET',
            self.url,
            Headers({'User-Agent': [ua]}),
            None)
        d.addCallback(self._on_response)
        d.addErrback(self._on_response_error)
        d.addBoth(self._on_finish)

    def _on_response(self, response):
        self.url = response.request.absoluteURI
        self.status = response.code

        if self.depth > 0 or self.test_case.need_page_source():
            Page.NUM += 1
            d = readBody(response)
            d.addCallback(self._on_body)
            d.addErrback(self._on_body_error)
            d.addBoth(self._on_finish)

        if not self.test_case.need_page_source():
            self.test_case.page_ready(self)

    def _on_body(self, body):
        self.page_source = body
        if self.depth > 0:
            self.test_case.extract_links(self)
        if self.test_case.need_page_source():
            self.test_case.page_ready(self)

    def _on_response_error(self, e):
        print "response error:", e.getErrorMessage(), "for url:", self.url

    def _on_body_error(self, e):
        print "read body error:", e.getErrorMessage(), "for url:", self.url

    def _on_finish(self, ignored):
        self.test_case.connection_close()
        Page.NUM -= 1
        if Page.NUM <= 0:
            self.test_case.finish()

    def __hash__(self):
        return self.url.__hash__()

    def __eq__(self, other):
        return self.url == other.url


class Result(object):
    __slots__ = ['page', 'msg']

    def __init__(self, page, msg):
        self.page = page
        self.msg = msg
