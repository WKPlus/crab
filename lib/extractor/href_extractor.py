# -*- coding:utf-8 -*-
"""
extractor for extracting links for a web page.

@author: qifa.zhao@dianping.com   xin.he@dianping.com
@license: Copyright (c) 2014 Dianping.com, Inc. All Rights Reserved

"""
import os
import sys
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "../")))
import re
from bs4 import BeautifulSoup
from lib.log import GLog
from lib.utils import fill_url, check_domain, get_url_detail


class Extractor(object):

    def __init__(self, valid_domains=("dianping.com", )):
        self.valid_domains = valid_domains
        self.trim = re.compile(" |\t|\n")

    def extract(self, url, content):
        u"""
        从page_source中提取所有的链接地址，作为一个set返回.
        如果传入valid_domains参数，则过滤掉域名不在valid_domains中的链接
        """
        soup = BeautifulSoup(content, "lxml")
        links = soup.find_all("a")
        INVALID_HREF = ("#", "javascript:")
        links = [re.sub(self.trim, "", l.attrs["href"]) for l in links
                 if "href" in l.attrs and l.attrs["href"] not in INVALID_HREF]

        protocol, host = get_url_detail(url)
        rel_links = set([protocol + "://" + host + l
                         for l in links if l.startswith("/")])
        abs_links = set([l for l in links if l.startswith("http")])

        if self.valid_domains:
            valid_abs_links = set([l for l in abs_links
                                   if check_domain(l, self.valid_domains)])
        else:
            valid_abs_links = abs_links

        links = rel_links.union(valid_abs_links)
        return [l.encode("utf-8") for l in links]


"""
这里简单记录一下使用html5lib和使用HTMLParser作为parser，
用BeautifulSoup解析网页提取所有link的效率差异.
测试页面: www.dianping.com/shanghai
测试工具: timeit
测试结果 (纯页面解析):
    使用HTMLParser作为parser，循环10次，耗时1.4-1.58秒
    使用html5lib作为parser，循环10次，耗时6.2-6.5秒
    使用lxml作为parser，循环10次，耗时1.38-1.56秒
测试结果 (页面解析+页面读取，包含网络交互):
    使用HTMLParser作为parser，循环10次，耗时7.5-7.7秒
    使用html5lib作为parser，循环10次，耗时11.6-11.7秒
    使用lxml作为parser，循环10次，耗时6.8-7.5秒
如何安装不同的parser以及不同的parser的优缺点比较，查看以下链接:
www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser
从效率和容错性方面来考虑，选择lxml作为parser

"""
