#!/usr/bin/env python
# encoding: utf-8
"""
@author: yanjianlong
@contact: yanjianlong@126.com
@time: 7/31/2016 9:58 PM
"""
from __future__ import print_function, unicode_literals
import datetime
import urllib2
import json

def get_data(symbol_string):
    url = "http://mdc.wallstreetcn.com/kline?prod_code=%s&candle_period=2&data_count=100&\
fields=min_time,open_px,close_px,high_px,low_px,business_amount,business_balance" %(symbol_string)
    req = urllib2.Request(url)
    response = urllib2.urlopen(req, timeout=1)
    return_data = json.loads(response.read())

    candle_dict = return_data.get("data", {}).get("candle", {})
    data_list = candle_dict.get(symbol_string, [])
    field_list = candle_dict.get("fields", [])
    if not field_list or not data_list:
        return None
    time_array = []
    close_array = []
    date_now = get_datetime_from_string("%s" %((data_list[-1][0])))
    for data in data_list:
        date_time = get_datetime_from_string("%s" %((data[0])))
        if not date_time:
            break
        if date_now.year == date_time.year and date_now.month == date_time.month and date_now.day == date_time.day:
            time_array.append(date_time)
            close_array.append(data[2])
    return time_array, close_array

def get_datetime_from_string(time_string):
    try:
        year = time_string[:4]
        month = time_string[4:6]
        day = time_string[6:8]
        hour = time_string[8:10]
        minute = time_string[10:]
        return datetime.datetime(int(year), int(month), int(day), int(hour), int(minute))
    except BaseException, e:
        print("yjl", time_string, e)
        return None

