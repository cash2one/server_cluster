# coding:utf-8
"""
    Created by 捡龙眼
    4/12/2016
"""

import time


WARNING_STRING = "warning"
SUCCESS_STRING = "success"
INFO_STRING = "info"
ERROR_STRING = "error"


class HomeInfo(object):
    def __init__(self):
        pass


class PageInfo(object):
    def __init__(self, page_number, page_link):
        self.page_number = page_number
        self.page_link = page_link


class ShortInfo(object):
    def __init__(self, info_id, short_tag, keys):
        self.flag = INFO_STRING
        time_second = time.localtime()
        self.create_time = time.strftime("%Y-%m-%d %H:%M:%S", time_second)
        self.id = info_id
        self.title = short_tag
        self.keys = keys

class PictureInfo(object):
    def __init__(self, pic_url, tag, pic_detail):
        self.pic_url = pic_url
        self.detail = pic_detail
        self.tag = tag
        self.active = False

    def set_active(self):
        self.active = True

def GetMorePageList():
    cur_page_list = [
        PageInfo(1, "/page/1"),
        PageInfo(2, "/page/2"),
        PageInfo(3, "/page/3"),
    ]
    return cur_page_list


def GetShortInfoList():
    short_list = [
        ShortInfo(1, "test1", "test1 test1 test1"),
        ShortInfo(2, "test2", "test2 test2 test2"),
        ShortInfo(3, "test3", "test3 test3 test3"),
        ShortInfo(4, "test4", "test4 test4 test4"),
        ShortInfo(5, "test5", "test5 test5 test5"),
        ShortInfo(6, "test6", "test6 test6 test6"),
    ]
    return short_list

def GetPictureShowList():
    pic_list = [
        PictureInfo("/static/img/1.jpg", "棒球", "棒球运动是一种以棒打球为主要特点，集体性、对抗性很强的球类运动项目，在美国、日本尤为盛行。"),
        PictureInfo("/static/img/2.jpg", "冲浪", "冲浪是以海浪为动力，利用自身的高超技巧和平衡能力，搏击海浪的一项运动。运动员站立在冲浪板上，或利用腹板、跪板、充气的橡皮垫、划艇、皮艇等驾驭海浪的一项水上运动。"),
        PictureInfo("/static/img/3.jpg", "自行车", "以自行车为工具比赛骑行速度的体育运动。1896年第一届奥林匹克运动会上被列为正式比赛项目。环法赛为最著名的世界自行车锦标赛。"),
    ]
    pic_list[0].set_active()
    return pic_list