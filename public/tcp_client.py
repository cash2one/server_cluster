# coding:utf-8
"""
    Created by 捡龙眼
    3/21/2016
"""
from __future__ import print_function, absolute_import, unicode_literals
import struct
import json
import tornado.tcpclient
import tornado.gen


class Connect(object):
    _HEAD_SIZE = 4

    def __init__(self):
        self._protocol = False
        self._data_buffer = ""
        self._protocol_content_length = self._HEAD_SIZE

    def get_address_flag(self):
        return self.__class__.__name__

    def start_server(self):
        raise NotImplementedError()

    def on_close_callback(self, data):
        raise NotImplementedError()

    def read_buffer_callback(self, size_buffer):
        self._data_buffer += size_buffer
        print(self.get_address_flag(), "read_buffer_callback", len(size_buffer))
        while self._data_buffer:
            if len(self._data_buffer) < self._protocol_content_length:
                break
            cur_content = self._data_buffer[:self._protocol_content_length]
            self._data_buffer = self._data_buffer[self._protocol_content_length:]
            if not self._protocol:
                self._protocol = True
                self._protocol_content_length = struct.unpack(b"!I", cur_content)[0] - self._HEAD_SIZE
            else:
                self._protocol = False
                self._protocol_content_length = self._HEAD_SIZE
                self.handle_process(cur_content)

    def handle_process(self, data):
        raise NotImplementedError()


class TcpClient(Connect):
    def __init__(self, io_loop, ip, port):
        Connect.__init__(self)
        self.__io_loop = io_loop
        self.__client = tornado.tcpclient.TCPClient()
        self.__ip = ip
        self.__port = port
        self.__stream = None

    def get_address_flag(self):
        return "target_server %s:%d" % (self.__ip, self.__port)

    @tornado.gen.coroutine
    def start_server(self):
        print("TcpClient start_client", self.__ip, self.__port)
        try:
            self.__stream = yield self.__client.connect(self.__ip, self.__port)
        except BaseException as e:
            self.add_time_callback()
            return
        self.on_auth_server()
        self.__stream.read_until_close(callback=self.on_close_callback, streaming_callback=self.read_buffer_callback)

    def on_auth_server(self):
        raise NotImplementedError()

    def send_data(self, data_dict):
        send_string = json.dumps(data_dict)
        data = struct.pack(b'!II', len(send_string) + 8, 1)
        self.__stream.write(data + send_string)

    def on_close_callback(self, data):
        self.add_time_callback()

    def handle_process(self, data):
        raise NotImplementedError()

    def add_time_callback(self):
        self.__io_loop.call_later(5, self.start_server)


