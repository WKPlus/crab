# -*- coding:utf-8 -*-
"""
utils

@author: qifa.zhao@dianping.com
@license: Copyright (c) 2013 Dianping.com, Inc. All Rights Reserved

"""

import os
import urllib
import re
import requests
import commands
from lib.log import GLog


def run_cmd(cmd):
    ret, output = commands.getstatusoutput(cmd)
    if ret != 0:
        GLog.warning("Run cmd[%s] failed! Error msg: %s", cmd, output)
    return ret, output


def read_list_from_file(file_name):
    if os.path.isfile(file_name):
        with open(file_name, "r") as in_fd:
            return [line.strip() for line in in_fd]
    else:
        GLog.warning("file[%s] not existed!", file_name)
        return []


def convert_chinese(url, pattern=r"[\x80-\xff]+"):
    #将url中的中文转义
    return re.sub(pattern, lambda s: urllib.quote(s.group()), url)


def fill_url(url):
    if url.startswith("http"):
        return url
    else:
        return "http://" + url


def get_url_detail(url):
    u"""从url提取出protocol和host.

    @return value:
        返回protocol,host二元组
        比如输入url为http://www.baidu.com/123/456返回(http,www.baidu.com)

    """
    if url.startswith("http"):
        protocol = url.split(":", 1)[0]
        host = url.split(":", 1)[1].strip("/").split("/", 1)[0]
    else:
        protocol = "http"
        host = url.split("/", 1)[0]
    return protocol, host


def get_status_code(url, ua):
    u"""下面这段代码在获取status code时有bug.

    使用链接:http://www.dianping.com/promo/208721#mod=4 进行测试时发现返回404
    但是浏览器访问该url一切正常
    headers={"User-Agent": USER_AGENT}
    try:
        url = fill_url(url)
        fd = urllib2.urlopen(urllib2.Request(url, headers = headers))
        return fd.getcode()
    except urllib2.HTTPError, e:
        return e.getcode()

    """
    #设置UA
    headers = {'User-Agent': ua}
    r = requests.get(fill_url(url), headers=headers)
    return r.url, r.status_code


def check_domain(url, valid_domains):
    u"""检查url对应的domain是否在预期的domain中.

    @return value: 如果url在预期domain中返回True，否则返回False

    """
    protocol, host = get_url_detail(url)
    for vd in valid_domains:
        if host.endswith(vd):
            return True
    return False
