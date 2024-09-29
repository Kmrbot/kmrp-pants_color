import enum


class PantsType(enum.Enum):
    PANTS_TYPE_SOLID = 0x000,   # 纯色
    PANTS_TYPE_FLOWER = 0x001,  # 花纹


class PantsColor(enum.Enum):
    PANTS_COLOR_NONE = 0, [""], [], []
    PANTS_COLOR_RED = 1, ["红色"], [0xFF0000], [PantsType.PANTS_TYPE_SOLID]
    PANTS_COLOR_GREEN = 20, ["绿色"], [0x00FF00], [PantsType.PANTS_TYPE_SOLID]
    PANTS_COLOR_BLUE = 30, ["蓝色"], [0x0000FF], [PantsType.PANTS_TYPE_SOLID]
    PANTS_COLOR_LIGHT_BLUE = 40, ["淡蓝色", "水色"], [0x00FFFF], [PantsType.PANTS_TYPE_SOLID]
    PANTS_COLOR_LIGHT_BLUE_FLOWER = 41, ["花纹淡蓝色"], [0x00FFFF], [PantsType.PANTS_TYPE_FLOWER]
    PANTS_COLOR_PURPLE = 50, ["紫色"], [0xFF00FF], [PantsType.PANTS_TYPE_SOLID]
    PANTS_COLOR_PINK = 60, ["粉色"], [0xFF80C0], [PantsType.PANTS_TYPE_SOLID]
    PANTS_COLOR_BLACK = 70, ["黑色"], [0x000000], [PantsType.PANTS_TYPE_SOLID]
    PANTS_COLOR_WHITE = 80, ["白色"], [0xFFFFFF], [PantsType.PANTS_TYPE_SOLID]
    PANTS_COLOR_GRAY = 90, ["灰色"], [0x646464], [PantsType.PANTS_TYPE_SOLID]
    PANTS_COLOR_GOLD = 100, ["金色"], [0xFFE640], [PantsType.PANTS_TYPE_SOLID]
    PANTS_COLOR_LAVENDER = 110, ["薰衣草色"], [0xB57EDC], [PantsType.PANTS_TYPE_SOLID]
    PANTS_COLOR_WHITE_PINK = 120, ["白色和粉色"], [0xFFFFFF, 0xFF80C0], [PantsType.PANTS_TYPE_SOLID, PantsType.PANTS_TYPE_SOLID]
    PANTS_COLOR_WHITE_PURPLE = 130, ["白色和紫色"], [0xFFFFFF, 0xFF00FF], [PantsType.PANTS_TYPE_SOLID, PantsType.PANTS_TYPE_SOLID]
    PANTS_COLOR_WHITE_PURPLE_FLOWER = 140, ["白色和紫色花纹"], [0xFFFFFF, 0xFF00FF], [PantsType.PANTS_TYPE_SOLID, PantsType.PANTS_TYPE_FLOWER]

    def __init__(self, color_value, color_names, colors, color_type):
        self.color_value = color_value
        self.color_names = color_names
        self.colors = colors
        self.color_type = color_type


def get_color_by_name(color_name: str):
    for color in PantsColor:
        if color_name in color.color_names:
            return color
    return None


def get_color_by_value(color_value: str):
    for color in PantsColor:
        if color.color_value == color_value:
            return color
    return None