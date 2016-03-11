# coding:utf-8
"""
    Created by 捡龙眼
    3/4/2016
"""
from __future__ import unicode_literals, print_function
import os
import traceback
import time
import sys
import datetime
import threading

import public.global_manager


DEBUG = "DEBUG"
INFO = "INFO"
WARNING = "WARNING"
ERROR = "ERROR"
FATAL = "FATAL"
CRITICAL = "CRITICAL"

LOG_PATH = "LOG_PATH"
SERVER_NAME = "SERVER_NAME"


def init_log_dir(log_path):
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    error_path = log_path + "/error_log"
    if not os.path.exists(error_path):
        os.mkdir(error_path)
    info_path = log_path + "/info_log"
    if not os.path.exists(info_path):
        os.mkdir(info_path)


def error_write(error_info):
    time_now = time.localtime()
    log_file_name = "%s/error_log/%s-%s-%02d-%02d-error.log" \
                    % (LOG_PATH, SERVER_NAME, time_now.tm_year,
                       time_now.tm_mon, time_now.tm_mday)
    logfile = open(log_file_name, 'a')
    error_msg = traceback.format_exc()
    traceback.print_exc(sys.__stderr__)
    error_head = "=" * 10 + time.ctime(time.time()) + '=' * 10
    log_error = "%s \n %s\n %s\n" % (error_head, error_info, error_msg)
    logfile.writelines(log_error)
    logfile.close()
    print(log_error)


class Log(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.__run = False
        self.__file_name = ""
        self.__file_object = None
        self.__log_string = []
        self.__lock = threading.Lock()
        self.__pre = "%s" % (SERVER_NAME)

    def run(self):
        self.__run = True
        print("log start!!!!!!!!!!!!!!!")
        self.__write_log_process()
        print("log end!!!!!!!!!!!!!!!")

    def __write_log_process(self):
        while self.__run:
            try:
                self.write_log_info()
            except BaseException, e:
                error_write(repr(e))

    def stop_thread(self):
        print(self.__class__.__name__, "stop!!!!!!!!!!")
        self.__run = False
        self.__write_log_process()

    def open_file(self):
        time_now = time.localtime()
        log_file_name = "%s/info_log/%s-%s-%02d-%02d.log" % (LOG_PATH, self.__pre,
                                                             time_now.tm_year, time_now.tm_mon, time_now.tm_mday)
        if self.__file_name == log_file_name:
            if not self.__file_object:
                self.__file_object = open(self.__file_name, "a+")
            return
        if self.__file_object:
            self.__file_object.close()
        self.__file_name = log_file_name
        self.__file_object = open(log_file_name, "a+")

    def write_log_info(self):
        if not self.__log_string:
            time.sleep(0.5)
            return

        self.__lock.acquire()
        log_string_info = self.__log_string
        self.__log_string = []
        self.__lock.release()

        self.open_file()
        for log_content in log_string_info:
            try:
                self.__file_object.write(log_content)
                print("yjl", log_content)
            except BaseException, e:
                error_write(e)
        self.__file_object.flush()

    def log_string(self, log_level, string_info):
        time_object = datetime.datetime.now()
        time_string = "%02d:%02d:%02d %03d" % (time_object.hour, time_object.minute,
                                               time_object.second, time_object.microsecond / 1000)
        self.__lock.acquire()
        self.__log_string.append("[%s %s]%s\n" % (time_string, log_level, string_info))
        self.__lock.release()


def log(log_level, content):
    public.global_manager.get_thread(public.global_manager.LOG_THREAD).log_string(log_level, content)


def info(content):
    log(INFO, content)


def initialize(log_path, server_name):
    global LOG_PATH
    global SERVER_NAME
    LOG_PATH, SERVER_NAME = log_path, server_name
    init_log_dir(log_path)
    log_instance = Log()
    log_instance.start()
    public.global_manager.add_thread(public.global_manager.LOG_THREAD, log_instance)


# if __name__ == "__main__":
# initialize()
# log(DEBUG, "DEBUG")

