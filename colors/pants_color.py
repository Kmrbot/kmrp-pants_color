import enum


class PantsType(enum.Enum):
    PANTS_TYPE_SOLID = 0x000,   # 纯色
    PANTS_TYPE_FLOWER = 0x001,  # 花纹


pants_color_data = {
    "红色": {
        "colors": [0xFF0000],
        "type": [PantsType.PANTS_TYPE_SOLID],
        "db_color": "红色",
    },
    "绿色": {
        "colors": [0x00FF00],
        "type": [PantsType.PANTS_TYPE_SOLID],
        "db_color": "绿色",
    },
    "蓝色": {
        "colors": [0x0000FF],
        "type": [PantsType.PANTS_TYPE_SOLID],
        "db_color": "蓝色",
    },
    "淡蓝色": {
        "colors": [0x00FFFF],
        "type": [PantsType.PANTS_TYPE_SOLID],
        "db_color": "淡蓝色",
    },
    "花纹淡蓝色": {
        "colors": [0x00FFFF],
        "type": [PantsType.PANTS_TYPE_FLOWER],
        "db_color": "花纹淡蓝色",
    },
    "水色": {
        "colors": [0x00FFFF],
        "type": [PantsType.PANTS_TYPE_SOLID],
        "db_color": "淡蓝色",
    },
    "紫色": {
        "colors": [0xFF00FF],
        "type": [PantsType.PANTS_TYPE_SOLID],
        "db_color": "紫色",
    },
    "粉色": {
        "colors": [0xFF80C0],
        "type": [PantsType.PANTS_TYPE_SOLID],
        "db_color": "粉色",
    },
    "黑色": {
        "colors": [0x000000],
        "type": [PantsType.PANTS_TYPE_SOLID],
        "db_color": "黑色",
    },
    "白色": {
        "colors": [0xFFFFFF],
        "type": [PantsType.PANTS_TYPE_SOLID],
        "db_color": "白色",
    },
    "灰色": {
        "colors": [0x646464],
        "type": [PantsType.PANTS_TYPE_SOLID],
        "db_color": "灰色",
    },
    "金色": {
        "colors": [0xFFE640],
        "type": [PantsType.PANTS_TYPE_SOLID],
        "db_color": "金色",
    },
    "薰衣草色": {
        "colors": [0xB57EDC],
        "type": [PantsType.PANTS_TYPE_SOLID],
        "db_color": "薰衣草色",
    },
    "白色和粉色": {
        "colors": [0xFFFFFF, 0xFF80C0],
        "type": [PantsType.PANTS_TYPE_SOLID, PantsType.PANTS_TYPE_SOLID],
        "db_color": "白色和粉色",
    },
    "白色和紫色": {
        "colors": [0xFFFFFF, 0xFF00FF],
        "type": [PantsType.PANTS_TYPE_SOLID, PantsType.PANTS_TYPE_SOLID],
        "db_color": "白色和紫色",
    },
    "白色和紫色花纹": {
        "colors": [0xFFFFFF, 0xFF00FF],
        "type": [PantsType.PANTS_TYPE_SOLID, PantsType.PANTS_TYPE_FLOWER],
        "db_color": "白色和紫色花纹",
    }
}
