# coding:utf-8
"""
    Created by 捡龙眼
    3/21/2016
"""

from __future__ import unicode_literals, print_function, absolute_import
import signal
import tornado.ioloop
import public.tcp_server
import public.global_manager
import public.simple_log
import public.tcp_client
import config

import client_logic.handle_client_process
import root_logic.handle_root_process
import root_logic.protocol


class ConnectRootServer(public.tcp_client.TcpClient):
    def __init__(self, io_loop, ip, port):
        public.tcp_client.TcpClient.__init__(self, io_loop, ip, port)

    def handle_process(self, data):
        root_logic.handle_root_process.handle_process(self, data)

    def on_auth_server(self):
        send_dict = {
            "server_type": config.SERVER_TYPE,
            "server_id": config.CLIENT_SERVER_ID,
            "token": "asdfghJkl1234567",
        }
        self.send_data(root_logic.protocol.ON_AUTH, send_dict)


class ClientServerConnect(public.tcp_server.ServerConnect):
    def handle_process(self, data):
        client_logic.handle_client_process.handle_process(self, data)

    def on_close_callback(self, data):
        print(self.get_address_flag(), "on_connect_close_process", len(data))


class ClientTcpServer(public.tcp_server.SimpleTcpServer):
    def create_server(self, stream, address):
        connect = ClientServerConnect(stream, address)
        return connect


def handle_terminal(signum=0, e=0):
    print("handle_terminal", signum, e)
    tornado.ioloop.IOLoop.instance().stop()
    public.global_manager.clear_thread()
    print("handle_terminal end")


def main():
    print(config.VERSION, config.SERVER_NAME, config.CLIENT_SERVER_PORT)
    public.simple_log.initialize(config.LOG_PATH, config.SERVER_NAME)
    signal.signal(signal.SIGINT, handle_terminal)
    signal.signal(signal.SIGTERM, handle_terminal)
    io_loop = tornado.ioloop.IOLoop.instance()
    public.tcp_server.initialize(io_loop)
    tcp_server = ClientTcpServer()
    tcp_server.listen(config.CLIENT_SERVER_PORT)

    tcp_client = ConnectRootServer(io_loop, config.ROOT_SERVER_IP, config.ROOT_SERVER_PORT)
    tcp_client.start_server()
    io_loop.start()


if __name__ == "__main__":
    main()