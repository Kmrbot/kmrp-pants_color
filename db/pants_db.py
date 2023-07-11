from tortoise.fields.data import CharField, IntField
from plugins.db_base_model import PluginsDBBaseModel


# 胖次颜色
class MiRiYaPantsColor(PluginsDBBaseModel):
    date = CharField(pk=True, max_length=32)        # 时间字符串 年.月.日
    color = CharField(max_length=16)                # 颜色
