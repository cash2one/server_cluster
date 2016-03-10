# coding:utf-8
"""
    捡龙眼
"""
from __future__ import unicode_literals, print_function, absolute_import
import tornado.web
import public.simple_log


class CommonRequest(tornado.web.RequestHandler):
    def process_request(self, process_obj, success_callback, error_callback):
        raise NotImplementedError()

    def initialize(self):
        pass  #just do any thing initalize

    def prepare(self):
        pass  # do anything before get/post

    def on_finish(self):
        pass  # call after the request

    def log_exception(self, type, value, tb):
        content = "Type:%s\nValue:%s\ntb:%s" % (type, value, tb)
        public.simple_log.error_write(content)

    def on_process(self, process_obj, success_callback, error_callback):
        """
        :param process_obj: public.task_process.Process
        :param success_callback:
        :param error_callback:
        :return:
        """
        process_obj.set_callback(success_callback, error_callback)
        process_obj.start_process()

    def success_callback(self, content):
        self.write(content)
        self.finish()

    def error_callback(self, error_flag):
        self.write_error(error_flag)


