# coding:utf-8
"""
    Created by 捡龙眼
    3/5/2016
"""
from __future__ import unicode_literals, print_function, absolute_import
import http_logic.common_response


class UserRegister(http_logic.common_response.CommonRequest):
    def get(self, *args, **kwargs):
        self.render("user/register.html")

    def post(self, *args, **kwargs):
        user_name = self.get_argument("user_name")
        password1 = self.get_argument("password1")
        password2 = self.get_argument("password2")
        self.render("user/login.html", title="test", user_name=user_name)