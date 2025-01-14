import datetime
from typing import Tuple, Any
from nonebot import on_regex
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.log import logger
from utils.permission import white_list_handle
from utils import get_time_zone
from .database.pants_color import DBPantsColorInfo
from .colors import get_user_data_by_user_name, get_pants_data_by_color_name, get_pants_data_by_color_value
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
    if get_user_data_by_user_name(name) is None:
        return await matcher.finish("无效目标名！")
    color_data = get_pants_data_by_color_name(color_str)
    if color_data is None:
        return await matcher.finish("无效颜色！")
    return name, date, color_data["value"]


@add_pants_color_record.handle()
async def _(matcher: Matcher,
            params: Tuple[Any, ...] = RegexGroup()):
    """添加胖次颜色记录"""
    results = await handle_pants_timestamp_color(matcher, params)

    name = results[0]
    date = results[1]
    new_color_value = results[2]
    new_color_name = get_pants_data_by_color_value(new_color_value)
    old_color_value = DBPantsColorInfo.get_pants_color(name, date)

    if old_color_value is not None:
        if old_color_value != new_color_value:
            old_color_data = get_pants_data_by_color_value(old_color_value)
            color_replace_str = (f"原记录颜色原记录被覆盖！原记录颜色："
                                 f"{old_color_data['color'][0] if old_color_data is not None else '未知'}\n\n")
        else:
            return await add_pants_color_record.finish(f"与原记录相同！")
    else:
        color_replace_str = ""
    is_success = DBPantsColorInfo.add_pants_color(name, date, new_color_value)
    await add_pants_color_record.finish(color_replace_str +
                                        f"已成功添加{name}胖次颜色记录： {date} 的胖次颜色为 {new_color_name['color'][0]}"
                                        if is_success else
                                        f"添加{name}胖次颜色记录失败")
