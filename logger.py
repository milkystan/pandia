
# -*- coding: utf-8 -*-
__author__ = 'Landleany'
import logging


log_format = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s", '%Y-%m-%d %H:%M:%S')
file_handler = logging.FileHandler(filename='pandia.log', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(log_format)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_format)
stream_handler.setLevel(logging.DEBUG)


def get_logger(name):
    log = logging.getLogger(name)
    log.addHandler(file_handler)
    log.addHandler(stream_handler)
    log.setLevel(logging.DEBUG)
    return log
