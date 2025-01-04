from nonebot import on_regex
from nonebot.rule import to_me
from protocol_adapter.adapter_type import AdapterMessageEvent
from utils.permission import white_list_handle
from protocol_adapter.protocol_adapter import ProtocolAdapter
from utils.task_deliver import TaskDeliverManager
from .colors import get_user_data_by_user_name, load_pants_color_data

get_pants_color_record = on_regex("胖次颜色列表",
                                  rule=to_me(),
                                  priority=5)
get_pants_color_record.__doc__ = """获取胖次颜色列表"""
get_pants_color_record.__help_type__ = None

get_pants_color_record.handle()(white_list_handle("pants_color"))


@get_pants_color_record.handle()
async def _(event: AdapterMessageEvent):
    """获取胖次颜色列表"""
    ret_str = "当前支持的颜色：\n"
    for data in load_pants_color_data()["info"]:
        ret_str += f"{data['color']}\n"
    await get_pants_color_record.finish(ret_str)
