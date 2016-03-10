# coding:utf-8
'''
    捡龙眼
'''
from __future__ import unicode_literals, print_function, absolute_import
import tornado.web
import tornado.httpclient
import tornado.gen

import http_logic.common_response
import public.task_process
import http_logic.http_request_task

#http://192.168.189.129:10000/index?

class IndexProcess(public.task_process.Process):
    def __init__(self):
        public.task_process.Process.__init__(self)

    def start_process(self):
        url = "https://github.com/yanjianlong"
        # url = "www.google.com"
        http_logic.http_request_task.add_multi_task(url, self.analyse_process, self.analyse_process)

    def analyse_process(self, response):
        if response.body is None:
            self.error_process(error_flag=404)
            return
        self.success_process(content=response.body)


class Index(http_logic.common_response.CommonRequest):
    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        self_process = IndexProcess()
        self.on_process(self_process, self.success_callback, self.error_callback)

    def post(self, *args, **kwargs):
        self_process = IndexProcess()
        self.on_process(self_process, self.success_callback, self.error_callback)
