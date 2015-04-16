#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
from selenium import webdriver
from bs4 import BeautifulSoup
from lib.log import GLog
from lib.reader import HTMLReader

"""
domain checker for scod.

@author: xin.he@dianping.com
@license: Copyright (c) 2013 Dianping.com, Inc. All Rights Reserved

"""


class DomainChecker(object):
    '''
    check all links at the given url by black or white list
    '''
    INVALID_HREF = ("#", "javascript:;", "javascript:void(0)", "javascript:")

    def __init__(self, whitelist=None, blacklist=None):
        self.whitelist = whitelist
        self.blacklist = blacklist
        self.html_reader = HTMLReader()
        self.err_msg = ''

    def check_by_whitelist(self, url):
        links = self.get_url_list(url)
        #count represent fail number
        count = 0
        for link in links:
            #获取url当中的host
            host = self.get_host_from_url(link)
            #flag=True represent domain is ok
            flag = False
            for domain in self.whitelist:
                if host.endswith(domain):
                    flag = True
                    break
            if not flag:
                count += 1
                self.err_msg += 'Domain not in whitelist [%s]\n' % link
                GLog.warning("Domain not in whitelist [%s], parent url: %s",
                             link, url)
        #count==0 represent no wrong
        if count == 0:
            return 0
        else:
            return 1

    def check_by_blacklist(self, url):
        links = self.get_url_list(url)
        #count represent fail number
        count = 0
        for link in links:
            #获取url当中的host
            host = self.get_host_from_url(link)

            for domain in self.blacklist:
                if host.endswith(domain):
                    count += 1
                    self.err_msg += 'Domain in blacklist [%s]\n' % link
                    GLog.warning("Domain in blacklist [%s], parent url:%s",
                                 link, url)
                    break
        #count==0 represent no wrong
        if count == 0:
            return 0
        else:
            return 1

    def get_host_from_url(self, url):
        #检查url是否以"http://"开头，若不是，加上
        if url.startswith('http://'):
            pass
        else:
            url = "http://" + url
        #获取url当中的host
        try:
            i = url.index(':')
            host = url[i + 3:][:url[i + 3:].index('/')]
        except ValueError:
            host = url[url.index(':') + 3:]
        return host

    def get_url_list(self, url, trim=re.compile(r"\s")):
        url, content = self.html_reader.read_content(url)
        soup = BeautifulSoup(content, "lxml")
        links = soup.find_all("a")
        #取出link并过滤掉非法link和相对路径的url
        links = [re.sub(trim, "", l.attrs["href"]) for l in links
                 if "href" in l.attrs and l.attrs["href"] not in
                 self.INVALID_HREF and not l.attrs["href"].startswith('/')]
        #去重操作
        links = list(set(links))
        return links

    def check(self, url):
        if self.whitelist is None and self.blacklist is None:
            GLog.fatal("You should input whitelist or blacklist at least")
            return 0
        v1 = 0
        if self.whitelist is not None:
            v1 = self.check_by_whitelist(url)
        v2 = 0
        if self.blacklist is not None:
            v2 = self.check_by_blacklist(url)
        if v1 + v2 == 0:
            return (0, '')
        else:
            return (1, self.err_msg)


if __name__ == "__main__":
    #Test code
#    dc = DomainChecker(blacklist=['dianping.com'])
    dc = DomainChecker(whitelist=['dianping.com'])
  #  dc = DomainChecker(blacklist=['zx110.org'])
  #  dc = DomainChecker()
    ret = dc.check(url="www.dianping.com/shanghai")
    print ret


