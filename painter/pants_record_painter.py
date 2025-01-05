import copy
import enum
import os
from typing import List, Dict, Tuple
import calendar
import datetime
import git
from PIL import Image, ImageDraw, ImageFont

from kmrbot.painter.pic_painter.color import Color
from kmrbot.painter.pic_painter.pic_generator import PicGenerator
from kmrbot.painter.pic_painter.utils import PainterUtils
from kmrbot.core.bot_base_info import KmrBotBaseInfo
from nonebot.log import logger
from .pants_record_border import PantsColorBorder
from utils import get_time_zone
from ..colors import get_pants_data_by_color_value


class PantsColorRecordType(enum.Enum):
    COLOR_TYPE_RECORD_OK = 0,
    COLOR_TYPE_RECORD_NO_RECORD = 1,
    COLOR_TYPE_RECORD_INVALID_COLOR = 2


class PantsRecordFont:
    __text_font = ImageFont.truetype(
        f"{PainterUtils.get_painter_resource_path()}/normal.ttf", 30)
    
    @classmethod
    def text_font(cls):
        return cls.__text_font


class PantsRecordPainter:
    @classmethod
    def generate_pants_record_pic(cls, name, bg_pic, pants_data):
        width = 1920
        height = 10000
        pic = PicGenerator(width, height)
        pic = pic.draw_rectangle(0, 0, width, height, Color.WHITE)

        # 绘制背景图
        pic = cls.__paint_background(pic, bg_pic)
        # 绘制标题内容
        pic = cls.__paint_title(name, pic)
        # 绘制标题内容
        pic = cls.__paint_pants_color_history(pic, pants_data)
        # 绘制统计数据
        pic = cls.__paint_statistics_data(pic, pants_data)
        # 设置当前的高度
        pic.set_height(pic.y + PantsColorBorder.BORDER_DESIGNER_INFO_BOTTOM_HEIGHT)
        # 绘制开发者信息
        pic = cls.__paint_designed_info(pic)

        pic.save("pants.png")
        return pic.bytes_io()

    @classmethod
    def __paint_background(cls, pic: PicGenerator, bg_pic):
        """ 绘制背景图 """
        pic.move_pos(0, 0)
        background_image = Image.open(f"{os.path.dirname(__file__)}/{bg_pic}")
        background_image = background_image.resize(
            (pic.width, int(background_image.height * pic.width / background_image.width))
        ).convert("RGBA")
        # 半透明
        translucent_image = Image.new("RGBA", background_image.size, (255, 255, 255, 160))
        background_image = Image.alpha_composite(background_image, translucent_image)

        pic.draw_img(background_image, pic.xy)
        # pic.set_height(background_image.height)
        return pic

    @classmethod
    def __paint_title(cls, name, pic: PicGenerator):
        """ 绘制标题 """
        pic.move_pos(0, 0)
        pic.paint_center_text(pic.x, f"{name}胖次颜色记录", PantsRecordFont.text_font(), Color.BLACK,
                              right_limit=pic.width,
                              row_length=0)
        return pic

    @classmethod
    def __paint_pants_color_history(cls, pic: PicGenerator, pants_data: List):
        """ 绘制胖次颜色历史记录 """
        pic.move_pos(-pic.x + PantsColorBorder.BORDER_PANTS_HISTORY_LR, PantsColorBorder.BORDER_TITLE_TO_HISTORY_B)
        if len(pants_data) == 0:
            return pic
        paint_data = copy.deepcopy(pants_data)
        paint_data.sort(key=lambda x: datetime.datetime.strptime(x["time"], "%Y.%m.%d").timestamp())   # 排序

        sys_datatime = datetime.datetime.now(get_time_zone())
        sys_year = sys_datatime.year
        sys_month = sys_datatime.month
        sys_day = sys_datatime.day
        
        cur_painting_year = None
        cur_painting_year_data = None
        for single_paint_data in paint_data:
            single_paint_data_datetime = datetime.datetime.strptime(single_paint_data["time"], "%Y.%m.%d")
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
            cur_painting_year_data[painting_month - 1][painting_day - 1] = single_paint_data["color"]
        pic = cls.__paint_pants_color_each_year(pic, cur_painting_year, cur_painting_year_data)
        return pic

    @classmethod
    def __paint_pants_color_each_year(cls, pic: PicGenerator, year, cur_year_data):
        """ 绘制每个年的胖次颜色历史记录 """
        pic.set_pos(PantsColorBorder.BORDER_PANTS_YEAR_L, pic.y)
        pic.paint_auto_line_text(pic.x, f"{year}年\n", PantsRecordFont.text_font(), Color.BLACK)
        for month in range(len(cur_year_data)):
            # 如果全空就不渲染了
            is_not_empty = False
            for color in cur_year_data[month]:
                if color != "":
                    is_not_empty = True
                    break
            if is_not_empty:
                pic.move_pos(0, PantsColorBorder.BORDER_PANTS_MONTH_D)
                pic = cls.__paint_pants_color_each_month(pic, year, month + 1, cur_year_data[month])
        pic.set_pos(PantsColorBorder.BORDER_PANTS_YEAR_L, pic.y)
        return pic

    @classmethod
    def __paint_pants_color_each_month(cls, pic: PicGenerator, year, month, cur_month_data):
        """ 绘制每个月的胖次颜色历史记录 """
        pic.set_pos(PantsColorBorder.BORDER_PANTS_MONTH_LR, pic.y + PantsColorBorder.BORDER_PANTS_DAY_D)
        pic.paint_auto_line_text(pic.x, f"{month}月\n", PantsRecordFont.text_font(), Color.BLACK)

        for each_day in range(len(cur_month_data)):
            # 渲染日期数字
            if each_day % 7 == 0 or each_day == len(cur_month_data) - 1:
                day_str = f"{each_day + 1}"
            else:
                day_str = ""
            pos_x = pic.x
            pic.paint_auto_line_text(pic.x, day_str, PantsRecordFont.text_font(), Color.BLACK)
            pic.set_pos(pos_x + 56, pic.y)
        pic.paint_auto_line_text(pic.x, "\n", PantsRecordFont.text_font(), Color.BLACK)
        pic.set_pos(PantsColorBorder.BORDER_PANTS_MONTH_LR, pic.y)
        for each_day in range(len(cur_month_data)):
            color = None
            color_value = cur_month_data[each_day]
            pants_pic = "pants/normal.png"  # 默认的
            if color_value == "":
                # 未记录
                color_type = PantsColorRecordType.COLOR_TYPE_RECORD_NO_RECORD
                pants_pic = "pants/未记录.png"  # 默认的
            else:
                color_data = get_pants_data_by_color_value(color_value)
                if color_data is None:
                    logger.warning(f"__paint_pants_color_each_month invalid color_data ! color_value = {color_value}")
                    color_type = PantsColorRecordType.COLOR_TYPE_RECORD_INVALID_COLOR
                else:
                    color_value = 0 if len(color_data["code"]) == 0 else int(color_data["code"][0], 16)  # 暂时先只画第1个颜色
                    pants_pic = color_data["pants_pic"]
                    color = ((color_value >> 16) & 0xff, (color_value >> 8) & 0xff, color_value & 0xff)
                    color_type = PantsColorRecordType.COLOR_TYPE_RECORD_OK
            pants_img = cls.__get_pants_pic(
                color_type,
                color,
                pants_pic,
                is_weekday=datetime.datetime.strptime(f"{year}.{month}.{each_day + 1}", "%Y.%m.%d").weekday() < 5)
            pic.move_pos(-15, 10)  # 图片向下移动一点会好看一些
            pic.paint_auto_line_pic(
                pic.x, pants_img, right_limit=pic.width - PantsColorBorder.BORDER_PANTS_DAY_LR)
            pic.move_pos(15, -10)
        pic.paint_auto_line_text(pic.x, "\n", PantsRecordFont.text_font())
        pic.set_pos(PantsColorBorder.BORDER_PANTS_MONTH_LR, pic.y)
        return pic

    @classmethod
    def __paint_statistics_data(cls, pic: PicGenerator, pants_data):
        """ 绘制统计数据 """
        pic.set_pos(PantsColorBorder.BORDER_PANTS_HISTORY_LR, pic.y + PantsColorBorder.BORDER_STATISTICS_U)
        pic.paint_auto_line_text(pic.x, "颜色统计：\n", PantsRecordFont.text_font(), Color.BLACK)
        if len(pants_data) == 0:
            return pic
        # 统计每种颜色的次数
        color_count = {}
        for each_pants_data in pants_data:
            if color_count.get(each_pants_data["color"]) is None:
                color_count[each_pants_data["color"]] = 0
            color_count[each_pants_data["color"]] += 1
        if len(color_count) != 0:
            arr = []
            for color_value, count in color_count.items():
                arr.append({"count": count, "color": color_value})
            arr.sort(key=lambda t: t["count"], reverse=True)
            for each_color_count_data in arr:
                count = each_color_count_data["count"]
                color_value = each_color_count_data["color"]
                # color_value = Color.BLACK  # 默认
                # if pants_color_data.get(color_str) is not None:
                #     color_value = pants_color_data[color_str]["colors"][0]  # 暂时先只画第1个颜色
                # color_value转颜色数据
                color_data = get_pants_data_by_color_value(color_value)
                color_data = color_data["color"][0] if color_data["color"] else "INVALID_COLOR"
                pic.paint_auto_line_text(pic.x, f"{color_data}：{count}次\n", PantsRecordFont.text_font(), Color.BLACK)

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
                            PantsRecordFont.text_font(),
                            [Color.DEEPSKYBLUE, Color.FUCHSIA, Color.CRIMSON, Color.BLACK, Color.RED, Color.GRAY])
        if len(KmrBotBaseInfo.get_author_name()) != 0:
            pic.draw_text_right(20, f"Author : {KmrBotBaseInfo.get_author_name()}", PantsRecordFont.text_font(),
                                Color.HELP_DESIGNER_AUTHOR_NAME)
        if len(KmrBotBaseInfo.get_author_url()) != 0:
            pic.draw_text_right(20, f"{KmrBotBaseInfo.get_author_url()}", PantsRecordFont.text_font(), Color.LINK)
        #pic.draw_text_right(20, f"Git Update SHA-1 : {git_commit_info['commit_id']}", PantsRecordFont.text_font(), Color.GREEN)
        #pic.draw_text_right(20, f"Git Update Date : {git_commit_info['date']}", PantsRecordFont.text_font(), Color.GREEN)
        pic.set_row_space(origin_row_space)

        return pic

    @classmethod
    def __get_pants_pic(cls, color_type, pants_color, pants_pic, is_weekday=False) -> Image:
        img_base_size = (56, 35)
        # 如果缓存有 就用缓存的
        dst_img = PantsRecordPainter.__pants_pic_cache.get((color_type, pants_color, pants_pic))
        if dst_img is None:
            img_base = Image.new("RGBA", img_base_size, (255, 255, 255, 0))
            if pants_color is not None:
                pants_size = (50, 25)
                pants_img = Image.open(f"{os.path.dirname(__file__)}/{pants_pic}")
                pants_img = pants_img.convert("RGBA")
                pants_img = pants_img.resize(pants_size)
                img_base.paste(pants_img, (3, 5))
            else:
                draw = ImageDraw.Draw(img_base)
                paint_pos = (20, -5)
                if color_type == PantsColorRecordType.COLOR_TYPE_RECORD_NO_RECORD:
                    draw.text(paint_pos, "？", Color.RED.value, font=PantsRecordFont.text_font())
                elif color_type == PantsColorRecordType.COLOR_TYPE_RECORD_INVALID_COLOR:
                    draw.text(paint_pos, "？", Color.GREEN.value, font=PantsRecordFont.text_font())
            PantsRecordPainter.__pants_pic_cache[(color_type, pants_color, pants_pic)] = img_base
            dst_img = img_base

        # dst_img = copy.deepcopy(dst_img)
        # 画一个外框
        # if is_weekday:
        #     side_border_img = Image.new("RGBA", img_base_size, (0, 0, 0, 255))
        #     # 掏空中间
        # else:
        #     side_border_img = Image.new("RGBA", img_base_size, (255, 0, 0, 255))
        # side_border_img_draw = ImageDraw.Draw(side_border_img)
        # side_border_img_draw.rectangle((2, 2, img_base_size[0] - 3, img_base_size[1] - 3), (255, 255, 255, 0), 2)
        # dst_img.alpha_composite(side_border_img)
        return dst_img

    __pants_pic_cache: Dict[Tuple[int, int, int], Image.Image] = {}   # Dict[Tuple[图片类型PantsColorType, 颜色color, 图片url], 图片]
