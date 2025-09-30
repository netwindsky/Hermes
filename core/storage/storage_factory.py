# storage_factory.py
import logging
from typing import Dict
from .data_storage import DataStorage
from .file_storage import FileStorage
from .mongodb_storage import MongoDBStorage  # 导入 MongoDBStorage

# 获取logger实例,用于日志记录
logger = logging.getLogger(__name__)

class StorageFactory:
    def __init__(self, config):
        self.config = config

    def create_storage(self):
        """根据配置创建存储实例"""
        storage_config = self.config.get('storage', {})
        storage_type = storage_config.get('type', 'file')

        if storage_type == 'mongodb':
            return MongoDBStorage(storage_config)
        else:
            return FileStorage(storage_config)
    @staticmethod
    def create(storage_type: str = 'file', **kwargs) -> DataStorage:
        """根据存储类型创建并返回相应的存储实例
    
        Args:
            storage_type (str): 存储类型,默认为'file'
            **kwargs: 其他参数,如 MongoDB 的 URI 和数据库名称
    
        Returns:
            DataStorage: 创建的存储实例
    
        Raises:
            ValueError: 如果不支持指定的存储类型,则抛出异常
        """
        if storage_type == 'file':
            # 如果请求的是文件存储类型,则返回FileStorage实例
            return FileStorage()
        elif storage_type == 'mongodb':
            # 如果请求的是 MongoDB 存储类型,则返回 MongoDBStorage 实例
            uri = kwargs.get('uri', 'mongodb://localhost:27017/')
            db_name = kwargs.get('db_name', 'hermes')
            username = kwargs.get('username', None)
            password = kwargs.get('password', None)
    
            print(f"创建 MongoDBStorage 实例, URI: {uri}, 数据库名称: {db_name}")
            return MongoDBStorage(uri=uri, db_name=db_name, username=username, password=password)
        # 可扩展其他存储类型
        else:
            raise ValueError(f"不支持的存储类型: {storage_type}")