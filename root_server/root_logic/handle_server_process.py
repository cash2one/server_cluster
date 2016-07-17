# coding:utf-8
"""
    Created by 捡龙眼
    3/21/2016
"""

from __future__ import print_function, unicode_literals, absolute_import
import struct
import public.pack_dict

import root_logic.protocol
import root_logic.auth


HANDLE_PROCESS = {
    root_logic.protocol.ON_AUTH: root_logic.auth.on_auth
}

def handle_process(conn, data):
    command = struct.unpack(b"!I", data[:4])[0]
    data = data[4:]
    content = public.pack_dict.loads_json_unicode(data)
    print(__name__, "handle_process", command, content)
    process = HANDLE_PROCESS.get(command)
    if not process:
        print(__name__, "handle_process no math", command, content)
        return
    process(conn, content)