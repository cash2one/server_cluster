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
import client_logic.protocol

class AuthClient(public.connect_data.Client):
    def __init__(self, client_id, conn):
        public.connect_data.Client.__init__(self, client_id, conn)


class AuthProcess(public.task_process.Process):
    def __init__(self, connect, uid, token):
        public.task_process.Process.__init__(self)
        self.__conn = connect
        self.__uid = uid
        self.__token = token

    def start_process(self):
        public.simple_log.info(self.__class__.__name__ + "start_process")
        self.success_process()


class AuthDataReceive(public.task_process.DataReceive):
    def __init__(self, conn, data):
        manager = public.global_manager.get_object(public.global_manager.WAITE_CONNECT_MANAGER)
        manager.del_connect(conn)
        self.__uid = data["uid"]
        self.__token = data["token"]
        self.__conn = conn

    def get_param(self):
        return self.__uid, self.__token, self.__conn

    def success_process(self, **kwargs):
        message = {"code": 0, "message": "成功"}
        message = public.pack_dict.dumps_json_to_utf8(message)
        self.__conn.send_message(struct.pack(b"!I", client_logic.protocol.ON_AUTH) + message)


@public.task_process.handle_process
def on_auth(conn, data_buffer):
    data_receive = AuthDataReceive(conn, data_buffer)
    uid, token, conn = data_receive.get_param()
    process = AuthProcess(conn, uid, token)
    return data_receive, process
