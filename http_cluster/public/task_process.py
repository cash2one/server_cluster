# coding:utf-8
"""
    Created by 捡龙眼
    3/4/2016
"""
from __future__ import absolute_import, print_function, unicode_literals

import time
import threading
import public.simple_log
import public.global_manager


class Process(object):
    def __init__(self):
        self.__success_callback = None
        self.__error_callback = None

    def success_process(self, **kwargs):
        if self.__success_callback:
            self.__success_callback(**kwargs)

    def error_process(self, **kwargs):
        if self.__error_callback:
            self.__error_callback(**kwargs)

    def set_callback(self, success_callback, error_callback):
        self.__success_callback = success_callback
        self.__error_callback = error_callback

    def start_process(self):
        raise NotImplementedError()


class Recv(object):
    def Unpack(self):
        pass

    def get_param(self):
        pass

    def handle_recv(self, process):
        process.set_callback(self.success_process)
        process.SetErrorCallback(self.error_process)
        process.start_process()

    def error_process(self, **kwargs):
        pass

    def success_process(self, **kwargs):
        pass


class MultiProcess(object):
    def __init__(self, key):
        self.__key = key
        self.__error_process = []
        self.__success_process = []
        self.__manager = None

    def start_process(self):
        raise NotImplementedError()

    def set_manager(self, manager):
        self.__manager = manager

    def get_key(self):
        return self.__key

    def add_process(self, success_process, error_process):
        self.__error_process.append(error_process)
        self.__success_process.append(success_process)

    def success_process(self, **kwargs):
        self.common_process(self.__success_process, **kwargs)

    def error_process(self, **kwargs):
        self.common_process(self.__error_process, **kwargs)

    def common_process(self, process_list, **kwargs):
        for callback in process_list:
            if not callback:
                continue
            try:
                callback(**kwargs)
            except BaseException as e:
                public.simple_log.error_write(repr(e))
        self.on_finish()

    def on_finish(self):
        if self.__manager:
            self.__manager.del_task(self.__key)
        self.__manager = None


class MultiProcessManager(object):
    def __init__(self):
        self.__manager = {}

    def add_process(self, key, success_callback, error_callback, *args, **kwargs):
        multi_process = self.__manager.get(key)
        if not multi_process:
            multi_process = self.get_multi_process(key, *args, **kwargs)
            multi_process.start_process()
            self.__manager[key] = multi_process
        multi_process.add_process(success_callback, error_callback)

    def get_multi_process(self, key, *args, **kwargs):
        raise NotImplementedError()

    def del_task(self, key):
        self.__manager.pop(key, None)


class Callback(object):
    def __init__(self, seq, time_out, callback, **kwargs):
        self.__time_out = time_out
        self.__seq = seq
        self.__callback = callback
        self.__kwargs = kwargs
        self.__time_begin = int(time.time())

    def get_seq(self):
        return self.__seq

    def __repr__(self):
        return "seq:%d, time_out:%d" % (self.__seq, self.__time_out)

    def error_callback(self):
        self.__callback(None, **self.__kwargs)

    def success_callback(self, package):
        self.__callback(package, **self.__kwargs)

    def out_of_time(self, time_now):
        time_interval = time_now - self.__time_begin
        return time_interval >= self.__time_out


class CallbackManager(object):
    def __init__(self, name):
        self.__name = name
        self.__dict = {}
        self.__delete = set()
        self.__lock = threading.Lock()

    def get_name(self):
        return self.__name

    def get_all_task(self):
        return self.__dict

    def add_callback(self, callback_obj):
        self.__lock.acquire()
        self.__dict[callback_obj.get_seq()] = callback_obj
        self.__lock.release()

    def pop_callback_by_seq(self, seq):
        self.__lock.acquire()
        obj = self.__dict.pop(seq)
        self.__lock.release()
        return obj

    def out_of_time_task(self, time_now):
        keys = set()
        for seq, obj in self.__dict.items():
            if obj.out_of_time(time_now):
                keys.add(seq)
                obj.error_callback()

        self.__lock.acquire()
        for key in keys:
            del self.__dict[key]
        self.__lock.release()


class TimerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.__time_before = int(time.time())
        self.__manager = {}
        self.__run = False

    def add_time_out_queue(self, manager):
        self.__manager[manager.get_name()] = manager

    def run(self):
        print(self.__class__.__name__, "start!!!!!!!!!!!!")
        self.__run = True
        while self.__run:
            try:
                time_now = int(time.time())
                time_interval = time_now - self.__time_before
                if time_interval < 1:
                    time.sleep(0.5)
                    time_now = int(time.time())
                self.__time_before = time_now
                for name, task_manager in self.__manager.items():
                    task_manager.out_of_time_task(time_now)

            except BaseException as e:
                public.simple_log.log(public.simple_log.ERROR, "error:%s \n" % (e))

    def stop_thread(self):
        print(self.__class__.__name__, "stop!!!!!!!!!!!!!")
        self.__run = False
        for name, task_manager in self.__manager.items():
            task_dict = task_manager.get_all_task()
            for key, task in task_dict.items():
                task.error_callback()


def initialize():
    time_instance = TimerThread()
    time_instance.start()
    public.global_manager.add_thread(public.global_manager.TIME_THREAD, time_instance)

