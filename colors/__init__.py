import enum
import json
from pathlib import Path

from utils.config import ensure_plugin_config_from_template

__NAME_TEMPLATE_PATH = Path(__file__).with_name("name_template.json")
__PANTS_COLOR_TEMPLATE_PATH = Path(__file__).with_name("pants_color_template.json")


# pants_color.json -> type
# 0 系统保留，不可手动录入
# 1 纯颜色
# 2 指定图片
class PantsColorType(enum.Enum):
    COLOR_TYPE_SYSTEM = 0
    COLOR_TYPE_PIC = 2


def load_name_data():
    path = ensure_plugin_config_from_template(
        "kmrp-pants_color",
        "name.json",
        __NAME_TEMPLATE_PATH,
    )
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_pants_color_data():
    path = ensure_plugin_config_from_template(
        "kmrp-pants_color",
        "pants_color.json",
        __PANTS_COLOR_TEMPLATE_PATH,
    )
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_user_data_by_user_name(user_name: str):
    for data in load_name_data()["info"]:
        if user_name == data["name"]:
            return data
    return None


def get_pants_data_by_color_name(color_name: str):
    for data in load_pants_color_data()["info"]:
        if color_name in data["color"] and data["type"] != PantsColorType.COLOR_TYPE_SYSTEM.value:
            return data
    return None


def get_pants_data_by_color_value(color_value: str):
    for data in load_pants_color_data()["info"]:
        if color_value == data["value"] and data["type"] != PantsColorType.COLOR_TYPE_SYSTEM.value:
            return data
    return None

def get_pants_last_time_by_user_name(user_name: str):
    for data in load_name_data()["info"]:
        if user_name == data["name"]:
            return data.get("last_time")
    return None
