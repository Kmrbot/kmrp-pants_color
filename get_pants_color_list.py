from nonebot import on_regex
from nonebot.rule import to_me
from protocol_adapter.adapter_type import AdapterMessageEvent
from utils.permission import white_list_handle
from .colors import load_pants_color_data

get_pants_color_list = on_regex("胖次颜色列表",
                                rule=to_me(),
                                priority=5)
get_pants_color_list.__doc__ = """获取胖次颜色列表"""
get_pants_color_list.__help_type__ = None

get_pants_color_list.handle()(white_list_handle("pants_color"))


@get_pants_color_list.handle()
async def _(event: AdapterMessageEvent):
    """获取胖次颜色列表"""
    ret_str = "当前支持的颜色：\n"
    for data in load_pants_color_data()["info"]:
        ret_str += f"{data['color']}\n"
    await get_pants_color_list.finish(ret_str)
