#-*- coding: utf8 -*-
import logging


def singleton(cls, instances={}):
    def get_ins(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_ins


@singleton
class Log(object):
    def __init__(self):
        self.logger = None
        self.stream_handler = None

    def init(self, name):
        if self.logger:
            return
        self.logger = logging.getLogger(name)
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)-6s > %(message)s',
            datefmt='%m-%d %H:%M:%S')

        file_handler = logging.FileHandler('./logs/%s.log' % name, mode='w')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)

        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setFormatter(formatter)
        self.stream_handler.setLevel(logging.INFO)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(self.stream_handler)
        self.logger.setLevel(logging.DEBUG)

    def set_sh_debug(self):
        if self.stream_handler:
            self.stream_handler.setLevel(logging.DEBUG)

    def check(func):
        def new_func(self, msg, *args):
            if not self.logger:
                return
            func(self, msg, *args)
        return new_func

    @check
    def debug(self, msg, *args):
        self.logger.debug(msg, *args)

    @check
    def info(self, msg, *args):
        self.logger.info(msg, *args)

    @check
    def warning(self, msg, *args):
        self.logger.warning(msg, *args)

    @check
    def error(self, msg, *args):
        self.logger.error(msg, *args)


GLog = Log()
