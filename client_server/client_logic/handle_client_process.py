# coding:utf-8
"""
    Created by 捡龙眼
    3/21/2016
"""
from __future__ import print_function, unicode_literals, absolute_import
import struct
import json

import client_logic.protocol
import client_logic.user.auth

HANDLE_PROCESS = {
    client_logic.protocol.ON_AUTH: client_logic.user.auth.on_auth,

}


def handle_process(conn, data):
    command = struct.unpack(b"!I", data[:4])[0]
    data = data[4:]
    content = json.loads(data)
    print(__name__, "handle_process", content)
    process = HANDLE_PROCESS.get(command)
    if not process:
        print(__name__, "handle_process no math", content)
        return
    process(conn, content)