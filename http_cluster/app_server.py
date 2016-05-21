# coding:utf-8
"""
    捡龙眼
    http server simple
"""
from __future__ import unicode_literals, print_function
import os
import sys
import signal

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket

import public.simple_log
import public.global_manager
import public.task_process
import http_logic.http_request_task
import http_logic.index
import http_logic.user.login
import http_logic.user.register
import http_logic.home

import config

HTTP_SERVER_NAME = "http_server"
PORT = 8888

class Home(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        page_list = http_logic.home.GetMorePageList()
        short_info_list = http_logic.home.GetShortInfoList()
        pic_info_list = http_logic.home.GetPictureShowList()
        self.render("home.html", page_list=page_list, short_info_list=short_info_list,
                    picture_show_info=pic_info_list)


class Compose(tornado.web.RequestHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render("compose.html")


class SocketListen(object):
    def __init__(self):
        self.__callbacks = []

    def register(self, callback):
        self.__callbacks.append(callback)
        print("add", callback)

    def un_register(self, callback):
        self.__callbacks.remove(callback)
        print("remove", callback)

    def notify(self, count):
        for callback in self.__callbacks:
            callback(count)
            count += 1


class WebSocketTest(tornado.websocket.WebSocketHandler):
    def open(self, *args, **kwargs):
        self.application.socket_listen.register(self.callback)

    def on_close(self):
        self.application.socket_listen.un_register(self.callback)

    def on_message(self, message):
        print("on_message", message)

    def callback(self, count):
        self.write_message("count:%d" % (count))


class HttpApplication(tornado.web.Application):
    URLS = [
        (r'/home', Home),
        (r'/compose', Compose),

        (r'/web_socket_test', WebSocketTest),

        (r'/index', http_logic.index.Index),
        (r'/user/login', http_logic.user.login.Login),
        (r'/user/register', http_logic.user.register.UserRegister),
    ]
    APP_SETTING = dict(
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True,
    )
    print(APP_SETTING)

    def __init__(self):
        tornado.web.Application.__init__(self, self.URLS, **self.APP_SETTING)
        self.__socket_listen = SocketListen()

    @property
    def socket_listen(self):
        return self.__socket_listen


def turn_down_server(signum=0, e=0):
    print("turn_down_server start!!!!!!!!", signum, e)
    tornado.ioloop.IOLoop.current().stop()
    public.global_manager.clear_thread()
    print("server turn_down_server finish!!!!!!!!!!!!!!!!!")


def main(port):
    signal.signal(signal.SIGTERM, turn_down_server)
    signal.signal(signal.SIGINT, turn_down_server)
    print(os.getcwd(), "server start", port, "version", config.VERSION)

    http_logic.http_request_task.initialize()

    public.simple_log.initialize(config.LOG_PATH, config.SERVER_NAME)
    public.task_process.initialize()

    app_server = HttpApplication()
    http_server = tornado.httpserver.HTTPServer(app_server)
    http_server.listen(port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    port = PORT
    if len(sys.argv) == 2:
        port = int(sys.argv[1])
    main(port)
