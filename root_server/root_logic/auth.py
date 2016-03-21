# coding:utf-8
"""
    Created by 捡龙眼
    3/13/2016
"""
from __future__ import unicode_literals, print_function, absolute_import
import struct

import public.pack_dict
import public.task_process
import public.global_manager
import public.simple_log
import public.connect_data
import config
import root_logic.protocol


class AuthClient(public.connect_data.Client):
    def __init__(self, client_id, conn):
        public.connect_data.Client.__init__(self, client_id, conn)


class AuthProcess(public.task_process.Process):
    def __init__(self, connect, server_id, server_type, token):
        public.task_process.Process.__init__(self)
        self.__conn = connect
        self.__server_id = server_id
        self.__server_type = server_type
        self.__token = token

    def start_process(self):
        public.simple_log.info(self.__class__.__name__ + "start_process")
        if self.__token == config.SERVER_TOKEN:
            auth_client = AuthClient(self.__server_id, self.__conn)
            auth_manager = public.global_manager.get_object(public.global_manager.AUTH_CONNECT_MANAGER)
            if auth_manager.on_auth(self.__server_type, self.__server_id, auth_client):
                self.success_process()
                return
        self.error_process()


class AuthDataReceive(public.task_process.DataReceive):
    def __init__(self, conn, data):
        manager = public.global_manager.get_object(public.global_manager.WAITE_CONNECT_MANAGER)
        manager.del_connect(conn)
        self.__server_type = data["server_type"]
        self.__server_id = data["server_id"]
        self.__token = data["token"]
        self.__conn = conn

    def get_param(self):
        return self.__server_type, self.__server_id, self.__token, self.__conn

    def success_process(self, **kwargs):
        message = {"code": 0, "message": "成功"}
        message = public.pack_dict.dumps_json_to_utf8(message)
        self.__conn.send_message(struct.pack(b"!I", root_logic.protocol.ON_AUTH) + message)

    def error_process(self, **kwargs):
        self.__conn.close_connect()


@public.task_process.handle_process
def on_auth(conn, data_buffer):
    data_receive = AuthDataReceive(conn, data_buffer)
    server_type, server_id, token, conn = data_receive.get_param()
    process = AuthProcess(conn, server_id, server_type, token)
    return data_receive, process
