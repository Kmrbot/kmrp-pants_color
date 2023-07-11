from nonebot import on_command
from nonebot.rule import to_me
from plugins import while_list_handle
from plugins.common_plugins_function import permission_only_me
from nonebot.adapters.onebot.v11.message import MessageSegment
from .db.pants_db_utils import PantsDBUtils
from .painter.pants_record_painter import PantsRecordPainter

get_pants_color_record_list = on_command("获取咪莉娅胖次颜色记录",
                                         rule=to_me(),
                                         priority=5)
get_pants_color_record_list.__doc__ = """获取咪莉娅胖次颜色记录"""
get_pants_color_record_list.__help_type__ = None

get_pants_color_record_list.handle()(while_list_handle("miriya_pants_color"))
get_pants_color_record_list.handle()(permission_only_me)


@get_pants_color_record_list.handle()
async def _():
    """获取咪莉娅胖次颜色记录"""
    pants_color_list = await PantsDBUtils.get_pants_color_list()
    message = MessageSegment.image(PantsRecordPainter.generate_pants_record_pic(pants_color_list))
    await get_pants_color_record_list.finish(message)
