# coding:utf-8
"""
    Created by 捡龙眼
    3/21/2016
"""

from __future__ import unicode_literals, print_function, absolute_import
import json

def dumps_json_to_utf8(data_dict):
    message = json.dumps(data_dict).encode("utf-8")
    return message

def loads_json_unicode(message_byte):
    message = byte2str(message_byte)
    data_dict = json.loads(message)
    return data_dict


def str2byte(data):
    return bytes(data, encoding="utf8")

def byte2str(bytes):
    return str(bytes, encoding="utf-8")
