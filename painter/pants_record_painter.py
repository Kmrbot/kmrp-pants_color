import copy
import enum
import json
import os
from typing import List
import calendar
import datetime
import git
from PIL import Image, ImageDraw

from kmrbot_plugins.painter.pic_painter.color import Color
from kmrbot_plugins.painter.pic_painter.pic_generator import PicGenerator
from kmrbot_plugins.bot_base_info import KmrBotBaseInfo
from nonebot.log import logger
from .pants_record_border import PantsColorBorder
from plugins.common_plugins_function import get_time_zone
from ..db.pants_db import MiRiYaPantsColor
from ..pants_color import pants_color_data


class PantsColorType(enum.Enum):
    COLOR_TYPE_OK = 0,
    COLOR_TYPE_NO_RECORD = 1,
    COLOR_TYPE_INVALID_COLOR = 2


class PantsRecordPainter:
    @classmethod
    def generate_pants_record_pic(cls, pants_data: List[MiRiYaPantsColor]):
        width = 1920
        height = 100000
        pic = PicGenerator(width, height)
        pic = pic.draw_rectangle(0, 0, width, height, Color.WHITE)

        # 绘制背景图
        pic = cls.__paint_background(pic)
        # 绘制标题内容
        pic = cls.__paint_title(pic)
        # 绘制标题内容
        pic = cls.__paint_pants_color_history(pic, pants_data)
        # 绘制统计数据
        pic = cls.__paint_statistics_data(pic, pants_data)
        # 绘制开发者信息
        pic = cls.__paint_designed_info(pic)

        return pic.bytes_io()

    @classmethod
    def __paint_background(cls, pic: PicGenerator):
        """ 绘制背景图 """
        pic.move_pos(0, 0)
        background_image = Image.open(f"{os.path.dirname(__file__)}/miriya.png")
        background_image = background_image.resize(
            (pic.width, int(background_image.height * pic.width / background_image.width))
        ).convert("RGBA")
        # 半透明
        translucent_image = Image.new("RGBA", background_image.size, (255, 255, 255, 160))
        background_image = Image.alpha_composite(background_image, translucent_image)

        pic.draw_img(background_image, pic.xy)
        pic.set_height(background_image.height)
        return pic

    @classmethod
    def __paint_title(cls, pic: PicGenerator):
        """ 绘制标题 """
        pic.move_pos(0, 0)
        pic.paint_center_text(pic.x, "咪莉娅胖次颜色记录", pic.base_text_font, Color.BLACK,
                              right_limit=pic.width,
                              row_length=0)
        return pic

    @classmethod
    def __paint_pants_color_history(cls, pic: PicGenerator, pants_data: List[MiRiYaPantsColor]):
        """ 绘制胖次颜色历史记录 """
        pic.move_pos(-pic.x + PantsColorBorder.BORDER_PANTS_HISTORY_LR, PantsColorBorder.BORDER_TITLE_TO_HISTORY_B)
        if len(pants_data) == 0:
            return pic
        paint_data = copy.deepcopy(pants_data)
        paint_data.sort(key=lambda x: datetime.datetime.strptime(x.date, "%Y.%m.%d").timestamp())   # 排序

        sys_datatime = datetime.datetime.now(get_time_zone())
        sys_year = sys_datatime.year
        sys_month = sys_datatime.month
        sys_day = sys_datatime.day
        
        cur_painting_year = None
        cur_painting_year_data = None
        for single_paint_data in paint_data:
            single_paint_data_datetime = datetime.datetime.strptime(single_paint_data.date, "%Y.%m.%d")
            painting_year = single_paint_data_datetime.year
            painting_month = single_paint_data_datetime.month
            painting_day = single_paint_data_datetime.day
            if painting_year != cur_painting_year:
                if cur_painting_year is not None:
                    # 绘制之前那一年的
                    pic = cls.__paint_pants_color_each_year(pic, cur_painting_year, cur_painting_year_data)
                    pic.move_pos(0, PantsColorBorder.BORDER_PANTS_YEAR_D)
                cur_painting_year = painting_year  # 设置新的年
                # 今年之前则每一个月都生成对应数量天数个空字符串
                # 今年则到今天为止的之前所有月都正常生成 本月则只生成到今天天数个
                # 后续年则不生成
                cur_painting_year_data = \
                    list([""
                          for _ in range(
                            calendar.monthrange(painting_year, month + 1)[1]
                            if (sys_year != painting_year or sys_month != (month + 1)) else sys_day)]
                         for month in range(
                        12
                        if sys_year > painting_year
                        else sys_month if sys_year == painting_year else 0))
            cur_painting_year_data[painting_month - 1][painting_day - 1] = single_paint_data.color
        pic = cls.__paint_pants_color_each_year(pic, cur_painting_year, cur_painting_year_data)
        return pic

    @classmethod
    def __paint_pants_color_each_year(cls, pic: PicGenerator, year, cur_year_data):
        """ 绘制每个年的胖次颜色历史记录 """
        pic.paint_auto_line_text(pic.x, f"{year}年\n", pic.base_text_font, Color.BLACK)
        for month in range(len(cur_year_data)):
            # 如果全空就不渲染了
            is_not_empty = False
            for color in cur_year_data[month]:
                if color != "":
                    is_not_empty = True
                    break
            if is_not_empty:
                pic.move_pos(0, PantsColorBorder.BORDER_PANTS_MONTH_D)
                pic = cls.__paint_pants_color_each_month(pic, month + 1, cur_year_data[month])
        return pic

    @classmethod
    def __paint_pants_color_each_month(cls, pic: PicGenerator, month, cur_month_data):
        """ 绘制每个月的胖次颜色历史记录 """
        pic.set_pos(PantsColorBorder.BORDER_PANTS_MONTH_LR, pic.y + PantsColorBorder.BORDER_PANTS_DAY_D)
        pic.paint_auto_line_text(pic.x, f"{month}月\n", pic.base_text_font, Color.BLACK)

        for each_day in range(len(cur_month_data)):
            # 渲染日期数字
            if each_day % 7 == 0 or each_day == len(cur_month_data) - 1:
                day_str = f"{each_day + 1}"
            else:
                day_str = ""
            pic.paint_auto_line_text(pic.x, day_str, pic.base_text_font, Color.BLACK)
            pic.set_pos(pic.x - pic.get_paint_string_length(day_str, pic.base_text_font)
                        + 50 + PantsColorBorder.BORDER_PANTS_DAY_EACH_PIC_R, pic.y)
        pic.paint_auto_line_text(pic.x, "\n", pic.base_text_font, Color.BLACK)
        pic.set_pos(PantsColorBorder.BORDER_PANTS_MONTH_LR, pic.y)
        for each_day in range(len(cur_month_data)):
            color = None
            color_str = cur_month_data[each_day]
            if color_str == "":
                # 未记录
                color_type = PantsColorType.COLOR_TYPE_NO_RECORD
            else:
                color_data = pants_color_data.get(color_str)
                if color_data is None:
                    logger.warning(f"__paint_pants_color_each_month invalid color_data ! color_str = {color_str}")
                    color_type = PantsColorType.COLOR_TYPE_INVALID_COLOR
                else:
                    color_value = color_data["colors"][0]  # 暂时先只画第1个颜色
                    color = ((color_value >> 16) & 0xff, (color_value >> 8) & 0xff, color_value & 0xff)
                    color_type = PantsColorType.COLOR_TYPE_OK
            pants_img = cls.__get_pants_pic(pic, color_type, color)
            pic.move_pos(0, 10)  # 图片向下移动一点会好看一些
            pic.paint_auto_line_pic(
                pic.x, pants_img, right_limit=pic.width - PantsColorBorder.BORDER_PANTS_DAY_LR)
            pic.move_pos(0, -10)
            pic.move_pos(PantsColorBorder.BORDER_PANTS_DAY_EACH_PIC_R, 0)
        pic.paint_auto_line_text(pic.x, "\n", pic.base_text_font)
        pic.set_pos(-PantsColorBorder.BORDER_PANTS_MONTH_LR, pic.y)
        return pic

    @classmethod
    def __paint_statistics_data(cls, pic: PicGenerator, pants_data: List[MiRiYaPantsColor]):
        """ 绘制统计数据 """
        pic.set_pos(PantsColorBorder.BORDER_PANTS_HISTORY_LR, pic.y + PantsColorBorder.BORDER_STATISTICS_U)
        pic.paint_auto_line_text(pic.x, "颜色统计：\n", pic.base_text_font, Color.BLACK)
        if len(pants_data) == 0:
            return pic
        # 统计每种颜色的次数
        color_count = {}
        for each_pants_data in pants_data:
            if color_count.get(each_pants_data.color) is None:
                color_count[each_pants_data.color] = 0
            color_count[each_pants_data.color] += 1
        if len(color_count) != 0:
            arr = []
            for color_str, count in color_count.items():
                arr.append({"count": count, "color": color_str})
            arr.sort(key=lambda t: t["count"], reverse=True)
            for each_color_count_data in arr:
                count = each_color_count_data["count"]
                color_str = each_color_count_data["color"]
                # color_value = Color.BLACK  # 默认
                # if pants_color_data.get(color_str) is not None:
                #     color_value = pants_color_data[color_str]["colors"][0]  # 暂时先只画第1个颜色
                # color_value转颜色数据
                pic.paint_auto_line_text(pic.x, f"{color_str}：{count}次\n", pic.base_text_font, Color.BLACK)

        return pic

    @classmethod
    def __paint_designed_info(cls, pic: PicGenerator):
        """ 绘制开发者信息 """
        pic.set_pos(0, pic.height - PantsColorBorder.BORDER_DESIGNER_INFO_BOTTOM_HEIGHT)   # 底端向上100

        # git提交信息
        repo = git.Repo(os.path.dirname(os.getcwd()))
        #git_commit_info = json.loads(repo.git.log('--pretty=format:{"commit_id":"%h", "date":"%cd", "summary":"%s"}',
        #                                          max_count=1))
        origin_row_space = pic.row_space
        pic.set_row_space(10)
        pic.draw_text_right(20,
                            ["K", "m", "r", "Bot", KmrBotBaseInfo.get_version()],
                            pic.base_text_font,
                            [Color.DEEPSKYBLUE, Color.FUCHSIA, Color.CRIMSON, Color.BLACK, Color.RED, Color.GRAY])
        pic.draw_text_right(20, f"Author : {KmrBotBaseInfo.get_author_name()}", pic.base_text_font,
                            Color.HELP_DESIGNER_AUTHOR_NAME)
        pic.draw_text_right(20, f"{KmrBotBaseInfo.get_author_url()}", pic.base_text_font, Color.LINK)
        #pic.draw_text_right(20, f"Git Update SHA-1 : {git_commit_info['commit_id']}", pic.base_text_font, Color.GREEN)
        #pic.draw_text_right(20, f"Git Update Date : {git_commit_info['date']}", pic.base_text_font, Color.GREEN)
        pic.set_row_space(origin_row_space)

        return pic

    @classmethod
    def __get_pants_pic(cls, pic, color_type, pants_color) -> Image:
        img = Image.open(f"{os.path.dirname(__file__)}/pants.png")
        img = img.convert("RGBA")
        img = img.resize((50, 25))
        d = img.getdata()
        new_image = []
        if pants_color is not None:
            for item in d:
                if item[0] > 200 and item[3] > 30:
                    new_image.append(pants_color)
                else:
                    new_image.append(item)
        else:
            draw = ImageDraw.Draw(img)
            paint_pos = (18, -8)
            if color_type == PantsColorType.COLOR_TYPE_NO_RECORD:
                draw.text(paint_pos, "？", Color.RED.value, font=pic.base_text_font)
            elif color_type == PantsColorType.COLOR_TYPE_INVALID_COLOR:
                draw.text(paint_pos, "？", Color.GREEN.value, font=pic.base_text_font)
        img.putdata(new_image)
        return img
