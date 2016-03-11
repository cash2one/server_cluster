# coding:utf-8
"""
    Created by 捡龙眼
    3/11/2016
"""
from __future__ import unicode_literals, print_function, absolute_import
import signal
import json
import struct

import tornado.ioloop

import public.tcp_server
import root_logic.user.auth
import public.global_manager
import public.simple_log
import config
import protocol

HANDLE_PROCESS = {
    protocol.ON_AUTH: root_logic.user.auth.on_auth
}


class RootServerConnect(public.tcp_server.ServerConnect):
    def handle_process(self, data):
        # try:
        command = struct.unpack(b"!I", data[:4])[0]
        data = data[4:]
        content = json.loads(data)
        print("handle_process", content)
        process = HANDLE_PROCESS.get(command)
        if not process:
            print("handle_process no math", content)
            return
        process(self, content)
        # except BaseException, e:
        #     print("handle_process error", e)

    def on_close_callback(self, data):
        print (self.get_address_flag(), "on_connect_close_process", len(data))

class RootTcpServer(public.tcp_server.SimpleTcpServer):
    def create_server(self, stream, address):
        connect = RootServerConnect(stream, address)
        return connect


def handle_terminal(signum=0, e=0):
    print("handle_terminal", signum, e)
    tornado.ioloop.IOLoop.instance().stop()
    public.global_manager.clear_thread()
    print("handle_terminal end")


def main():
    port = 8888
    print(config.VERSION, config.SERVER_NAME, port)
    public.simple_log.initialize(config.LOG_PATH, config.SERVER_NAME)
    signal.signal(signal.SIGINT, handle_terminal)
    signal.signal(signal.SIGTERM, handle_terminal)
    io_loop = tornado.ioloop.IOLoop.instance()
    public.tcp_server.initialize(io_loop)
    tcp_server = RootTcpServer()
    tcp_server.listen(port)
    io_loop.start()


if __name__ == "__main__":
    main()