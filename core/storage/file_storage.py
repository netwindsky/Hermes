import json
from urllib.parse import urlparse
import logging
import os
from typing import Dict
from .data_storage import DataStorage

# 获取logger实例,用于日志记录
logger = logging.getLogger(__name__)

class FileStorage(DataStorage):
    """文件存储实现"""
    def __init__(self, storage_config=None):
        self.storage_config = storage_config or {}
        self.base_path = self.storage_config.get('path', 'data')
    def save(self, table_name: str, data: Dict):
        """保存数据到文件

        Args:
            data (Dict): 需要保存的数据字典,包含url等信息
        """
        try:
            # 检查并创建 data 目录
            if not os.path.exists('data'):
                os.makedirs('data')
            # 根据数据中的url生成文件名
            filename = table_name + '.txt'
            # 打开文件,准备写入
            with open(f'data/{filename}', 'a', encoding='utf-8') as f:
                # 将数据保存为JSON格式到文件中,确保非ASCII字符能正确处理
                f.write(json.dumps(data, ensure_ascii=False) + '\n')
            # 记录日志,数据保存成功
            logger.info(f"数据已保存到 {filename}")
        except Exception as e:
            # 异常处理,记录日志,数据保存失败
            logger.error(f"文件存储失败: {str(e)}")
    async def close(self):
        """关闭文件存储，由于使用了with语句自动关闭文件，这里不需要额外操作"""
        pass