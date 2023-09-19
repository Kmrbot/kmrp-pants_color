import datetime
import re
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import (
    Message,
)
from nonebot.params import ArgPlainText, CommandArg
from plugins.common_plugins_function import get_time_zone, white_list_handle
from .db.pants_db_utils import PantsDBUtils
from .pants_color import pants_color_data

add_pants_color_record = on_command("添加咪莉娅胖次颜色记录",
                                    rule=to_me(),
                                    priority=5)
add_pants_color_record.__doc__ = """添加咪莉娅胖次颜色记录"""
add_pants_color_record.__help_type__ = None

add_pants_color_record.handle()(white_list_handle("miriya_pants_color"))


async def handle_pants_timestamp_color(
    matcher: Matcher,
    command_arg: Message = CommandArg(),
):
    data = command_arg.extract_plain_text().split(' ')
    if len(data) == 1:
        # 时间是今天
        date = datetime.datetime.now(get_time_zone()).strftime("%Y.%m.%d")
        color_str = data[0]
    elif len(data) == 2:
        try:
            datetime_param = datetime.datetime.strptime(data[0], "%Y.%m.%d")
        except ValueError:
            try:
                datetime_param = datetime.datetime.strptime(data[0], "%Y/%m/%d")
            except ValueError:
                return await matcher.finish("时间格式错误！正确格式：年.月.日 或 年/月/日")
        date = datetime_param.strftime("%Y.%m.%d")
        color_str = data[1]
    else:
        return await matcher.finish("无效参数！参数列表：时间（可省略） + 颜色名")
    if pants_color_data.get(color_str) is None:
        return await matcher.finish("无效颜色！")

    matcher.set_arg("date", Message(date))
    matcher.set_arg("color", Message(color_str))
add_pants_color_record.handle()(handle_pants_timestamp_color)


@add_pants_color_record.handle()
async def _(date: str = ArgPlainText("date"), color: str = ArgPlainText("color")):
    """添加咪莉娅胖次颜色记录"""
    old_color = await PantsDBUtils.get_pants_color(date=date)
    if old_color is not None:
        if old_color.color != color:
            color_replace_str = f"原记录颜色原记录被覆盖！原记录颜色：{old_color.color}\n\n"
        else:
            color_replace_str = f"与原记录相同！\n\n"
    else:
        color_replace_str = ""
    await PantsDBUtils.set_pants_color(date=date, color=color)
    await add_pants_color_record.finish(color_replace_str + f"已成功添加咪莉娅胖次颜色记录： {date} 的胖次颜色为 {color}")
