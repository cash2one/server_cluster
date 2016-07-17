# coding:utf-8
"""
    Created by 捡龙眼
    3/21/2016
"""
from __future__ import absolute_import, print_function, unicode_literals
import public.global_manager

class Client(object):
    def __init__(self, client_id, conn_object):
        self._client_id = client_id
        self._connect = conn_object

    def on_close(self):
        self._connect.close_connect()


class ClientManager(object):
    def __init__(self, client_type):
        self.__type = client_type
        self.__client = {}

    def get_conn_by_id(self, client_id):
        return self.__client.get(client_id)

    def on_auth(self, client_id, client_object):
        old_conn = self.get_conn_by_id(client_id)
        if old_conn:
            old_conn.on_close()
            print(self, "on_auth", client_id, "re_auth")
        self.__client[client_id] = client_object


class AuthManager(object):
    def __init__(self, type_list):
        self.__manager = {}
        for client_type in type_list:
            self.__manager[client_type] = ClientManager(client_type)

    def on_auth(self, client_type, client_id, client_object):
        client_manager = self.__manager.get(client_type)
        if not client_manager:
            print(self, "on_auth no type", client_type)
            return False
        client_manager.on_auth(client_id, client_object)
        return True


def initialize(type_list):
    manager = AuthManager(type_list)
    public.global_manager.add_object(public.global_manager.AUTH_CONNECT_MANAGER, manager)

