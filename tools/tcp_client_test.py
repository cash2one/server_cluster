# coding:utf-8
"""
    Created by 捡龙眼
    3/13/2016
"""
import struct
import socket
import json
import time


def get_send_data(cmd, send_dict):
    send_string = json.dumps(send_dict)
    data = struct.pack('!II', len(send_string) + 8, cmd)
    return data + send_string


def resolveRecvdata(data):
    head = struct.unpack('!2I', data[:8])
    length = head[0]
    data_content = data[8:length]
    data_dict = json.loads(data_content)
    print("resolveRecvdata", head, data_dict)
    return data_dict


def test_auth(the_socket, logic_id, platform):
    the_socket.connect(('localhost', 8888))
    data = get_auth_package(logic_id, platform)
    time.sleep(20)

    the_socket.send(data)
    data = the_socket.recv(1024)
    data = resolveRecvdata(data)
    print data


def get_auth_package(logic_id, platform):
    send_dict = {
        "uid": logic_id,
        "token": "token",
        "platform": platform,
    }
    return get_send_data(1, send_dict)


if __name__ == "__main__":
    begin = time.time()
    socket_list = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for i in xrange(1)]
    test_auth(socket_list[0], 2041718105, "pc")
    # for logic_id in xrange(3):
    #     for platform in xrange(2):
    #         if platform == 0:
    #             test_auth(socket_list[logic_id * 2 + platform], logic_id, "pc")
    #         else:
    #             test_auth(socket_list[logic_id * 2 + platform], logic_id, "cc")
    for the_scoket in socket_list:
        the_scoket.close()
    print "time_cose:", time.time() - begin

