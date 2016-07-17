# coding:utf-8
"""
    Created by 捡龙眼
    3/5/2016
"""

from __future__ import unicode_literals, print_function, absolute_import

import http_logic.common_response

class Login(http_logic.common_response.CommonRequest):
    def get(self, *args, **kwargs):
        self.render("user/login.html", title="测试 test title", user_name="测试user_name")

    def post(self, *args, **kwargs):
        pass