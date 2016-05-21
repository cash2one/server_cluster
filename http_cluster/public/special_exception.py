# coding:utf-8
"""
Created by yanjianlong on 3/4/2016
"""
from __future__ import unicode_literals, print_function


class CommonException(Exception):
    def __init__(self, msg):
        self.__error_info = msg
        print(self.__str__())

    def __str__(self):
        return self.__class__.__name__ + ":" + self.__error_info

    __repr__ = __str__


class KeyExistError(CommonException):
    pass