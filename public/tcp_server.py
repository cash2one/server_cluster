# coding:utf-8
"""
    Created by 捡龙眼
    3/12/2016
"""
from __future__ import absolute_import, print_function, unicode_literals
import functools
import heapq
import struct
import time

import tornado.tcpserver
import tornado.ioloop

import public.global_manager


OUT_OF_TIME = 10


class WaiteConnectManager(object):
    def __init__(self):
        self.__connects = []

    def add_connect(self, tcp_connect):
        heapq.heappush(self.__connects, tcp_connect)

    def remove_old_socket(self, io_loop):
        # print(self, "remove_old_socket start", self.__connects)
        time_now = int(time.time())
        while self.__connects:
            if self.__connects[0].bool_time_out(time_now):
                connect = heapq.heappop(self.__connects)
                connect.close_connect()
                # print(self, "remove_old_socket ing", connect)
            else:
                break
        # print(self, "remove_old_socket end", self.__connects)
        io_loop.call_later(OUT_OF_TIME, self.remove_old_socket, io_loop)


    def del_connect(self, connect):
        # print("del_connect", self.__connects, connect)
        if connect in self.__connects:
            self.__connects.remove(connect)
        # print("del_connect finish", len(self.__connects))
        heapq.heapify(self.__connects)


def initialize(io_loop):
    waite_connect_manager = WaiteConnectManager()
    public.global_manager.add_object(public.global_manager.WAITE_CONNECT_MANAGER, waite_connect_manager)
    io_loop.call_later(OUT_OF_TIME, waite_connect_manager.remove_old_socket, io_loop)


class ServerConnect(object):
    _HEAD_SIZE = 4

    def __init__(self, stream, address):
        self.__address = address
        self.__stream = stream
        self.__stream.set_close_callback(self.on_connect_close)
        self.__connect_time = int(time.time())

    @property
    def connect_time(self):
        return self.__connect_time

    def get_address_flag(self):
        return "%s:%d" % (self.__address[0], self.__address[1])

    def on_connect_close(self):
        # print(self.get_address_flag(), "close>>>>>>>>>>>")
        self.clean_waite()
        self.on_connect_close_process()

    def on_connect_close_process(self):
        pass

    def clean_waite(self):
        waite_connect_manager = public.global_manager.get_object(public.global_manager.WAITE_CONNECT_MANAGER)
        waite_connect_manager.del_connect(self)

    def start_server(self):
        # print(self.get_address_flag(), "start_server")
        waite_connect_manager = public.global_manager.get_object(public.global_manager.WAITE_CONNECT_MANAGER)
        waite_connect_manager.add_connect(self)
        self.read_head_size()

    def send_message(self, data):
        send_content = struct.pack(b"!I", len(data) + self._HEAD_SIZE) + data
        self.__stream.write(send_content)

    def read_head_size(self):
        # print(self.get_address_flag(), "read_head_size")
        callback = functools.partial(self.read_buffer_callback, self._HEAD_SIZE)
        self.__stream.read_bytes(self._HEAD_SIZE, streaming_callback=callback)

    def read_buffer_callback(self, head_size, size_buffer):
        if not self.check_buff_size(head_size, len(size_buffer)):
            return
        size = struct.unpack(b"!I", size_buffer)[0] - head_size
        if size < 0:
            print("read_buffer_callback error")
            return
        # print(self.get_address_flag(), "read_buffer_callback", size, size_buffer)
        callback = functools.partial(self.handle_receive, size)
        self.__stream.read_bytes(size, streaming_callback=callback)

    def handle_receive(self, size, data):
        # print(self.get_address_flag(), "handle_receive", len(data))
        if not self.check_buff_size(size, len(data)):
            return
        self.handle_process(data)
        self.read_head_size()
        # print(self.get_address_flag(), "handle_receive error", size, len(data))

    def handle_process(self, data):
        raise NotImplementedError()

    def check_buff_size(self, need_size, receive_size):
        if need_size == receive_size:
            return True
        else:
            # self.__stream.close()
            print("check_buff_size error", need_size, receive_size)
            return False

    def close_connect(self):
        self.__stream.close()

    def bool_time_out(self, time_now):
        if time_now - self.__connect_time > OUT_OF_TIME:
            return True
        return False

    def __le__(self, other):
        # print("le", self.connect_time, other.connect_time)
        return self.connect_time < other.connect_time

    def __lt__(self, other):
        # print("lt", self.connect_time, other.connect_time)
        return self.connect_time <= other.connect_time


class SimpleTcpServer(tornado.tcpserver.TCPServer):
    # def __init__(self, io_loop=None, ssl_options=None, max_buffer_size=None, read_chunk_size=None):
    # tornado.tcpserver.TCPServer.__init__(self, io_loop, ssl_options, max_buffer_size, read_chunk_size)
    def handle_stream(self, stream, address):
        connect = self.create_server(stream, address)
        connect.start_server()

    def create_server(self, stream, address):
        raise NotImplementedError()



