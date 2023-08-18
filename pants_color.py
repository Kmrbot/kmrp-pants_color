import enum


class PantsType(enum.Enum):
    PANTS_TYPE_SOLID = 0x000,   # 纯色
    PANTS_TYPE_FLOWER = 0x001,  # 花纹


pants_color_data = {
    "红色": {
        "colors": [0xFF0000],
        "type": PantsType.PANTS_TYPE_SOLID,
    },
    "绿色": {
        "colors": [0x00FF00],
        "type": [PantsType.PANTS_TYPE_SOLID],
    },
    "蓝色": {
        "colors": [0x0000FF],
        "type": [PantsType.PANTS_TYPE_SOLID],
    },
    "淡蓝色": {
        "colors": [0x00FFFF],
        "type": [PantsType.PANTS_TYPE_SOLID],
    },
    "花纹淡蓝色": {
        "colors": [0x00FFFF],
        "type": [PantsType.PANTS_TYPE_FLOWER],
    },
    "水色": {
        "colors": [0x00FFFF],
        "type": [PantsType.PANTS_TYPE_SOLID],
    },
    "紫色": {
        "colors": [0xFF00FF],
        "type": [PantsType.PANTS_TYPE_SOLID],
    },
    "粉色": {
        "colors": [0xFF80C0],
        "type": [PantsType.PANTS_TYPE_SOLID],
    },
    "黑色": {
        "colors": [0x000000],
        "type": [PantsType.PANTS_TYPE_SOLID],
    },
    "白色": {
        "colors": [0xFFFFFF],
        "type": [PantsType.PANTS_TYPE_SOLID],
    },
    "灰色": {
        "colors": [0x646464],
        "type": [PantsType.PANTS_TYPE_SOLID],
    },
    "金色": {
        "colors": [0xFFE640],
        "type": [PantsType.PANTS_TYPE_SOLID],
    },
    "薰衣草色": {
        "colors": [0xB57EDC],
        "type": [PantsType.PANTS_TYPE_SOLID],
    },
    "白色和粉色": {
        "colors": [0xFFFFFF, 0xFF80C0],
        "type": [PantsType.PANTS_TYPE_SOLID, PantsType.PANTS_TYPE_SOLID],
    },
    "白色和紫色": {
        "colors": [0xFFFFFF, 0xFF00FF],
        "type": [PantsType.PANTS_TYPE_SOLID, PantsType.PANTS_TYPE_SOLID],
    },
    "白色和紫色花纹": {
        "colors": [0xFFFFFF, 0xFF00FF],
        "type": [PantsType.PANTS_TYPE_SOLID, PantsType.PANTS_TYPE_FLOWER],
    }
}
