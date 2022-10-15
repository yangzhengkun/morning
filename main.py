#!/usr/bin/env python3

import os
import math
import random

from datetime import datetime
from zhdate import ZhDate
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage
import requests

start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']
app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]
user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


# app_id = "wx5f31e726a6edbc5c"
# app_secret = "15c02c0ba826265bbbc3272871eb9fb9"
# birthday = "04-29"
# start_date = "2021-10-07"
# user_id = "ohdhv57YjAEY7OnK97gd7U6-ipUg"
# template_id = "IU7XOfI4lp8Q_1ZBZqpfPC9cDdzudr2oyucchwGzdLM"

def get_weather():
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + "开江"
    res = requests.get(url).json()
    weather = res['data']['list'][0]
    return f"{weather['weather']}，{weather['low']}℃~{weather['high']}℃", math.floor(weather['temp'])


def get_days_count():
    delta = datetime.now() - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days


def get_birthday():
    month, day = birthday.strip("-")
    month = int(month.strip()) if month.isdigit() else 4
    day = int(day.strip()) if day.isdigit() else 29
    lunar_today = ZhDate.today()
    this_year_birthday = ZhDate(lunar_today.lunar_year, month, day)
    next_year_birthday = ZhDate(lunar_today.lunar_year + 1, month, day)
    return (this_year_birthday - lunar_today) if this_year_birthday - lunar_today > 0 else next_year_birthday - lunar_today


def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']


def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


def get_date():
    week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    weekday = week_list[datetime.now().weekday()]
    return f"{datetime.now().strftime('%Y-%m-%d')}，{ZhDate.today()}，{weekday}"


if __name__ == '__main__':
    client = WeChatClient(app_id, app_secret)
    wm = WeChatMessage(client)

    wea, temperature = get_weather()
    data = {
        "date": {
            "value": get_date()
        },
        "weather": {
            "value": wea
        },
        "love_days": {
            "value": get_days_count()
        },
        "birthday_left": {
            "value": get_birthday()
        },
        "words": {
            "value": get_words(),
            "color": get_random_color()
        }
    }

    res = wm.send_template(user_id, template_id, data)
    print(res)
