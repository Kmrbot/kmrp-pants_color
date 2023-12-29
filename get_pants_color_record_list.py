from typing import Tuple, Any
from nonebot import on_regex
from nonebot.rule import to_me
from utils.permission import white_list_handle
from protocol_adapter.protocol_adapter import ProtocolAdapter
from .database.pants_color import DBPantsColorInfo
from .painter.pants_record_painter import PantsRecordPainter
from nonebot.params import RegexGroup
from .colors.names import names
from utils.permission import only_me

get_pants_color_record_list = on_regex("^获取(.*)胖次颜色记录$",
                                       rule=to_me(),
                                       priority=5)
get_pants_color_record_list.__doc__ = """获取胖次颜色记录"""
get_pants_color_record_list.__help_type__ = None

get_pants_color_record_list.handle()(white_list_handle("pants_color"))
get_pants_color_record_list.handle()(only_me)


@get_pants_color_record_list.handle()
async def _(params: Tuple[Any, ...] = RegexGroup()):
    """获取咪莉娅胖次颜色记录"""
    name = params[0]
    if name not in names or names[name]["name"] is None:
        await get_pants_color_record_list.finish("无效目标名！")
    pants_color_list = DBPantsColorInfo.get_pants_color_list(names[name]["name"])
    message = ProtocolAdapter.MS.image(PantsRecordPainter.generate_pants_record_pic(
        names[name]["name"],
        names[name]["bg_pic"],
        pants_color_list))
    await get_pants_color_record_list.finish(message)
