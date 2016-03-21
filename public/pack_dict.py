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

def loads_json_unicode(message):
    data_dict = json.loads(message)
    return data_dict
