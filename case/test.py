# -*- coding:utf-8 -*-

"""
sample test cases for scod.
These test cases can be either in one .py file or in mutil .py file.

@author: qifa.zhao@dianping.com
@license: Copyright (c) 2013 Dianping.com, Inc. All Rights Reserved

"""

from lib.case import TestCase
#import checkers needed here
from checker.http import HTTPStatusChecker

class TestCase1(TestCase):
    u""" simplest test case: 测试www.baidu.com的http状态码是否为200 """
    def __init__(self):
        self.add_url("www.baidu.com")
        self.add_checker(HTTPStatusChecker(200))

class TestCase2(TestCase):
    u""" 测试www.dianping.com/shanghai以及其一层子链接的http状态码是否为200 """
    def __init__(self):
        self.add_url("www.dianping.com/shanghai", 1)
        self.add_checker(HTTPStatusChecker(200))

class TestCase3(TestCase):
    u"""
    测试www.zhihu.com以及其下域名为zhihu.com的一层子链接http状态码是否为200
    """
    def __init__(self):
        self.add_url("www.zhihu.com", 1)
        from lib.extractor.href_extractor import Extractor
        self.add_link_extractor(Extractor(valid_domains=("zhihu.com",)))
        self.add_checker(HTTPStatusChecker(200))

