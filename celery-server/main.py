#!/usr/bin/env python
# encoding: utf-8
"""
@author: yanjianlong
@contact: yanjianlong@126.com
@time: 7/19/2016 9:28 PM
"""

import urllib.request
import bs4
import bs4.element
import time
import send_msg.weixin

class GetFirstElement(object):
    def __init__(self):
        self.__url = "http://kx.fx678.com/"
        self.__headers = ('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')

    def get_html_page(self):
        opener = urllib.request.build_opener()
        opener.addheaders = [self.__headers]
        return opener.open(self.__url).read()

    def has_class_id_level(self, tag):
        return tag.has_attr("class") and tag.has_attr("id") and tag.has_attr("level")

    def get_first_element(self):
        data = self.get_html_page()
        bs4_obj = bs4.BeautifulSoup(data, "html.parser")
        result = bs4_obj.find_all(self.has_class_id_level, limit=1)
        if not result:
            return None
        return result[0]

def get_last_time_content():
    obj = GetFirstElement()
    element = obj.get_first_element()
    time_content, result = "", ""
    if element != None:
        time_content = element.find_all("div", class_="gray_text", limit=1)[0].contents[0]
        contents = element.find_all("div", class_="gray_font", limit=1)[0].contents
        for content in contents:
            if isinstance(content, bs4.element.Tag):
                continue
            # if re.search(r"<.*>", content, re.M|re.I):
            #     continue
            result += content
    return time_content, result

def main():
    last_time = ""
    while True:
        time_string, content = get_last_time_content()
        if last_time != time_string:
            last_time = time_string
            send_msg.weixin.get_weixin_instance().sendMsg("CTO Club", content, False)
            print(last_time, content)
        time.sleep(20)

if __name__ == "__main__":
    main()
