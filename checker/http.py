# -*- coding:utf-8 -*-

"""
http status checker

@author: qifa.zhao@dianping.com
@license: Copyright (c) 2013 Dianping.com, Inc. All Rights Reserved

"""

import os
import sys
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "../")))
from lib.log import GLog


class HTTPStatusChecker(object):
    fields = ['status']

    def __init__(self, expect=200):
        self.expect = expect

    def is_status_expected(self, status_code):
        #judge whether status code is expected
        if callable(self.expect):
            return self.expect(status_code)
        elif isinstance(self.expect, int):
            return self.expect == status_code
        elif isinstance(self.expect, tuple):
            return status_code in self.expect

        #this should never happen! It means you give HTTPStatusChecker an
        #invalid parameter for expect.
        return True

    def check(self, page):
        if self.is_status_expected(page.status):
            return True, None
        else:
            GLog.warning("Status code[%s] not expected for url: %s",
                         page.status, page.url)
            return False, "Unexpected status code %s" % page.status
