from typing import Tuple, Any
from nonebot import on_regex
from nonebot.rule import to_me
from protocol_adapter.adapter_type import AdapterMessageEvent
from utils.permission import white_list_handle
from protocol_adapter.protocol_adapter import ProtocolAdapter
from utils.push_manager import PushManager
from utils.task_deliver import TaskDeliverManager
from .database.pants_color import DBPantsColorInfo
from .painter.pants_record_painter import PantsRecordPainter
from nonebot.params import RegexGroup
from .colors import get_user_data_by_user_name
from utils.permission import only_me

get_pants_color_record_list = on_regex("^获取(.*)胖次颜色记录$",
                                       rule=to_me(),
                                       priority=5)
get_pants_color_record_list.__doc__ = """获取胖次颜色记录"""
get_pants_color_record_list.__help_type__ = None

get_pants_color_record_list.handle()(white_list_handle("pants_color"))
get_pants_color_record_list.handle()(only_me)


def generate_pic_task(**kwargs):
    name = kwargs["name"]
    bg_pic = kwargs["bg_pic"]
    pants_color_list = DBPantsColorInfo.get_pants_color_list(name)
    push_data = PushManager.PushData(
        msg_type=kwargs["msg_type"],
        msg_type_id=kwargs["msg_type_id"],
        message=ProtocolAdapter.MS.image(PantsRecordPainter.generate_pants_record_pic(name, bg_pic, pants_color_list))
    )
    PushManager.notify(push_data)


@get_pants_color_record_list.handle()
async def _(event: AdapterMessageEvent, params: Tuple[Any, ...] = RegexGroup()):
    """获取咪莉娅胖次颜色记录"""
    name = params[0]
    user_data = get_user_data_by_user_name(name)
    if user_data is None:
        await get_pants_color_record_list.finish("无效目标名！")
    TaskDeliverManager.add_task(
        generate_pic_task,
        name=name,
        bg_pic=user_data["bg_pic"],
        msg_type=ProtocolAdapter.get_msg_type(event),
        msg_type_id=ProtocolAdapter.get_msg_type_id(event))
    await get_pants_color_record_list.finish("正在绘制中...")
