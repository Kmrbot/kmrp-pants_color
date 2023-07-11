import enum


class PantsType(enum.Enum):
    PANTS_TYPE_FLOWER = 0x001,  # 花纹


pants_color_data = {
    "红色": {
        "colors": [0xFF0000]
    },
    "绿色": {
        "colors": [0x00FF00]
    },
    "蓝色": {
        "colors": [0x0000FF]
    },
    "淡蓝色": {
        "colors": [0x00FFFF]
    },
    "花纹淡蓝色": {
        "colors": [0x00FFFF],
        "type": PantsType.PANTS_TYPE_FLOWER,
    },
    "水色": {
        "colors": [0x00FFFF]
    },
    "紫色": {
        "colors": [0xFF00FF]
    },
    "粉色": {
        "colors": [0xFF80C0]
    },
    "黑色": {
        "colors": [0x000000]
    },
    "白色": {
        "colors": [0xFFFFFF]
    },
    "灰色": {
        "colors": [0x646464]
    },
    "金色": {
        "colors": [0xFFE640]
    },
    "薰衣草色": {
        "colors": [0xB57EDC]
    },
    "白色和粉色": {
        "colors": [0xFFFFFF, 0xFF80C0]
    },
    "白色和紫色": {
        "colors": [0xFFFFFF, 0xFF00FF]
    }
}
