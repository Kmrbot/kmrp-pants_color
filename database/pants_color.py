import copy
import re
from database.interface.db_impl_interface import DBImplInterface
from database.db_manager import DBManager


# B站翻译信息
class DBPantsColorInfo(DBImplInterface):

    """
    key: {name}
    """
    _default_value = {
    }

    @classmethod
    def get_pants_color(cls, name, date):
        """ 获取胖次颜色 """
        key = cls.generate_key(name)
        data = cls.get_data_by_key(key)
        return data.get(date) if data else None

    @classmethod
    def add_pants_color(cls, name, date, color):
        """ 添加胖次颜色 """
        key = cls.generate_key(name)
        data = cls.get_data_by_key(key)
        if data is None:
            data = copy.deepcopy(cls._default_value)
        data[date] = color
        cls.set_data(key, data)

    @classmethod
    def get_pants_color_list(cls, name):
        """ 获取胖次颜色列表 """
        key = cls.generate_key(name)
        data = cls.get_data_by_key(key)
        ret_data = []
        for key, single_data in data.items():
            ret_data.append({
                "time": key,
                "color": single_data
            })
        return ret_data

    @classmethod
    def db_key_name(cls, bot_id):
        # 公共的
        return f"{cls.__name__}"

    @classmethod
    async def init(cls):
        """ 初始化 """
        pass

    @classmethod
    def generate_key(cls, name):
        """ 生成__data内存放的key """
        return f"{name}"

    @classmethod
    def analysis_key(cls, key):
        """ 解析generate_key生成的key """
        regex_groups = re.match("([a-zA-Z0-9_]*)", key).groups()
        if regex_groups is not None:
            return {
                "name": regex_groups[0]
            }


DBManager.add_db(DBPantsColorInfo)
