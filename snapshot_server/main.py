#!/usr/bin/env python
# encoding: utf-8
"""
@author: yanjianlong
@contact: yanjianlong@126.com
@time: 7/31/2016 9:58 PM
"""
import matplotlib.pyplot
import matplotlib.dates
import get_data

def create_picture(symbol):
    daysFmt = matplotlib.dates.DateFormatter('%H:%M')
    fig, ax1 = matplotlib.pyplot.subplots()
    fig.set_size_inches(10, 5)
    date_list, close_list = get_data.get_data(symbol)
    if not close_list:
        return
    high, low = close_list[0], close_list[0]
    for close in close_list:
        if close > high:
            high = close
        elif close < low:
            low = close
    ax1.plot(date_list, close_list, color="gray")
    ax1.xaxis.set_major_formatter(daysFmt)
    # ax1.set_ylim(low - 0.01, high + 0.01)
    ax1.autoscale_view()
    matplotlib.pyplot.setp(matplotlib.pyplot.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    matplotlib.pyplot.show()
    # matplotlib.pyplot.savefig("test.png", dpi=40)

if __name__ == "__main__":
    symbol = "002202.SZ"
    create_picture(symbol)