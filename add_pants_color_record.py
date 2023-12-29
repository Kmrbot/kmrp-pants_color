import datetime
from typing import Tuple, Any
from nonebot import on_regex
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.log import logger
from utils.permission import white_list_handle
from utils import get_time_zone
from .database.pants_color import DBPantsColorInfo
from .colors.pants_color import pants_color_data
from .colors.names import names
from nonebot.params import RegexGroup

add_pants_color_record = on_regex("^添加(.*)胖次颜色记录 +([^ ]*) *([^ ]*)? *$",
                                  rule=to_me(),
                                  priority=5)
add_pants_color_record.__doc__ = """添加胖次颜色记录"""
add_pants_color_record.__help_type__ = None

add_pants_color_record.handle()(white_list_handle("pants_color"))


async def handle_pants_timestamp_color(matcher: Matcher, params) -> Tuple[str, str, str]:
    if len(params) != 3:
        logger.error(f"handle_pants_timestamp_color params size invalid ! size = {len(params)}")
        return await matcher.finish(f"无效参数数量！当前参数数量：{len(params)}")
    if len(params[0]) == 0 or len(params[1]) == 0:
        logger.error(f"handle_pants_timestamp_color params invalid name or color ! params = {params}")
        return await matcher.finish("错误的名称或颜色！")
    elif len(params[2]) == 0:
        # 时间是今天
        name = params[0]
        date = datetime.datetime.now(get_time_zone()).strftime("%Y.%m.%d")
        color_str = params[1]
    else:
        name = params[0]
        try:
            datetime_param = datetime.datetime.strptime(params[1], "%Y.%m.%d")
        except ValueError:
            try:
                datetime_param = datetime.datetime.strptime(params[1], "%Y/%m/%d")
            except ValueError:
                return await matcher.finish("时间格式错误！正确格式：年.月.日 或 年/月/日")
        date = datetime_param.strftime("%Y.%m.%d")
        color_str = params[2]
    if name not in names or names[name].get("name") is None:
        return await matcher.finish("无效目标名！")
    color_data = pants_color_data.get(color_str)
    if color_data is None:
        return await matcher.finish("无效颜色！")
    return names[name]["name"], date, color_data["db_color"]


@add_pants_color_record.handle()
async def _(matcher: Matcher,
            params: Tuple[Any, ...] = RegexGroup()):
    """添加胖次颜色记录"""
    results = await handle_pants_timestamp_color(matcher, params)

    name = results[0]
    date = results[1]
    color = results[2]
    old_color = DBPantsColorInfo.get_pants_color(name, date)
    if old_color is not None:
        if old_color != color:
            color_replace_str = f"原记录颜色原记录被覆盖！原记录颜色：{old_color}\n\n"
        else:
            return await add_pants_color_record.finish(f"与原记录相同！")
    else:
        color_replace_str = ""
    DBPantsColorInfo.add_pants_color(name, date, color)
    await add_pants_color_record.finish(color_replace_str + f"已成功添加{name}胖次颜色记录： {date} 的胖次颜色为 {color}")
