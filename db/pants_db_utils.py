import os
from pathlib import Path
from typing import List
from nonebot import get_driver
from tortoise import Tortoise
from tortoise.connection import connections
from plugins.common_plugins_function import get_plugin_db_path
from .pants_db import MiRiYaPantsColor


class PantsDBUtils:

    @classmethod
    async def init(cls):
        plugin_name = os.path.split(Path(os.path.dirname(os.path.dirname(__file__))))[1]
        config = {
            "connections": {
                "plugin_miriya_pants_color_conn": f"sqlite://{get_plugin_db_path('miriya_pants_color.sqlite3')}"
            },
            "apps": {
                "kmr_bot_app": {
                    "models": [f"plugins.{plugin_name}.db.pants_db"],
                    "default_connection": "plugin_miriya_pants_color_conn",
                }
            }
        }

        await Tortoise.init(config)
        await Tortoise.generate_schemas()

    @classmethod
    async def get_pants_color_list(cls) -> List[MiRiYaPantsColor]:
        """ 获取胖次颜色列表 """
        return await MiRiYaPantsColor.get()

    @classmethod
    async def get_pants_color(cls, **kwargs):
        """ 获取胖次颜色 """
        return await MiRiYaPantsColor.get(**kwargs)

    @classmethod
    async def set_pants_color(cls, **kwargs):
        """ 设置胖次颜色 """
        if not await cls.get_pants_color(**kwargs):
            await MiRiYaPantsColor.add(
                date=kwargs["date"],
                color=kwargs["color"])
        else:
            await MiRiYaPantsColor.update(
                {
                    "date": kwargs["date"]},
                color=kwargs["color"])


get_driver().on_startup(PantsDBUtils.init)
# get_driver().on_shutdown(connections.close_all)
