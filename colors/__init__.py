import json
import os.path
from typing import Optional
from nonebot.log import logger


def load_name_data():
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "name.json"), encoding="utf-8") as f:
        return json.load(f)


def load_pants_color_data():
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "pants_color.json"), encoding="utf-8") as f:
        return json.load(f)


def get_user_data_by_user_name(user_name: str):
    for data in load_name_data()["info"]:
        if user_name == data["name"]:
            return data
    return None


def get_pants_data_by_color_name(color_name: str):
    for data in load_pants_color_data()["info"]:
        if color_name in data["color"]:
            return data
    return None


def get_pants_data_by_color_value(color_value: str):
    for data in load_pants_color_data()["info"]:
        if color_value == data["value"]:
            return data
    return None
