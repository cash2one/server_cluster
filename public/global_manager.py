# coding:utf-8
"""
    Created by 捡龙眼
    3/4/2016
"""
from __future__ import absolute_import, unicode_literals, print_function
import public.special_exception


LOG_THREAD = "log_thread"
TIME_THREAD = "time_thread"

GLOBAL_THREAD = {}


def add_thread(key, thread_object):
    if key in GLOBAL_THREAD:
        raise public.special_exception.KeyExistError("%s is exist" % (key))
    GLOBAL_THREAD[key] = thread_object


def get_thread(key):
    return GLOBAL_THREAD.get(key)


def clear_thread():
    for thread_object in GLOBAL_THREAD.values():
        try:
            thread_object.stop_thread()
        except BaseException, e:
            print(e)


HTTP_REQUEST_MANAGER = "http_request_manager"
WAITE_CONNECT_MANAGER = "waite_client_manager"
AUTH_CONNECT_MANAGER = "auth_connect_manager"

GLOBAL_OBJECT = {}


def add_object(key, object):
    if key in GLOBAL_OBJECT:
        raise public.special_exception.KeyExistError("%s is exist" % (key))
    GLOBAL_OBJECT[key] = object


def get_object(key):
    return GLOBAL_OBJECT.get(key)