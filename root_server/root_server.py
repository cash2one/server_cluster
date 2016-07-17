# coding:utf-8
"""
    Created by 捡龙眼
    3/11/2016
"""
from __future__ import unicode_literals, print_function, absolute_import
import signal

import tornado.ioloop

import public.tcp_server
import public.global_manager
import public.simple_log
import public.tcp_client
import public.connect_data
import config
import root_logic.handle_server_process

class RootServerConnect(public.tcp_server.ServerConnect):
    def handle_process(self, data):
        root_logic.handle_server_process.handle_process(self, data)

    def on_close_callback(self, data):
        print(self.get_address_flag(), "on_connect_close_process", len(data))


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
    print(config.VERSION, config.SERVER_NAME, config.ROOT_SERVER_PORT)
    public.simple_log.initialize(config.LOG_PATH, config.SERVER_NAME)
    signal.signal(signal.SIGINT, handle_terminal)
    signal.signal(signal.SIGTERM, handle_terminal)
    io_loop = tornado.ioloop.IOLoop.instance()
    public.tcp_server.initialize(io_loop)
    public.connect_data.initialize(config.CLIENT_TYPE_LIST)
    tcp_server = RootTcpServer()
    tcp_server.listen(config.ROOT_SERVER_PORT)
    io_loop.start()


if __name__ == "__main__":
    main()