import logging
from typing import Dict

# 获取logger实例,用于日志记录
logger = logging.getLogger(__name__)

class DataStorage:
    """数据存储抽象类,定义保存数据的接口"""
    def save(self, data: Dict):
        # 抽象方法,子类必须实现
        raise NotImplementedError