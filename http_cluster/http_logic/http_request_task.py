# coding:utf-8
"""
Created by 捡龙眼
"""
from __future__ import absolute_import, print_function, unicode_literals
import urllib
import tornado.httpclient
import tornado.gen
import public.task_process
import public.global_manager


def get_http_request_task_key(url, **kwargs):
    key = urllib.quote(url)
    if kwargs:
        key = "%s%s" % (key, urllib.urlencode(kwargs))
    return key


class MultiRequestTask(public.task_process.MultiProcess):
    def __init__(self, key, url, **kwargs):
        public.task_process.MultiProcess.__init__(self, key)
        self.__http_request = tornado.httpclient.HTTPRequest(url, **kwargs)

    @tornado.gen.coroutine
    def start_process(self):
        http_client = tornado.httpclient.AsyncHTTPClient()
        http_client.fetch(self.__http_request, self.finish_request)

    def finish_request(self, response):
        if response.body is None:
            self.error_process(response=response)
        else:
            self.success_process(response=response)


class CRequestManager(public.task_process.MultiProcessManager):
    def get_multi_process(self, key, *args, **kwargs):
        url = args[0]
        task = MultiRequestTask(key, url, **kwargs)
        task.set_manager(self)
        return task


def initialize():
    manager = CRequestManager()
    public.global_manager.add_object(public.global_manager.HTTP_REQUEST_MANAGER, manager)


def add_multi_task(url, success_callback, error_callback, **kwargs):
    key = get_http_request_task_key(url, **kwargs)
    manager = public.global_manager.get_object(public.global_manager.HTTP_REQUEST_MANAGER)
    manager.add_process(key, success_callback, error_callback, url, **kwargs)

