
import asyncio  # 导入 asyncio 模块
import threading
import logging
import json
import jsonpath
from bs4 import BeautifulSoup
from core.storage.data_storage import DataStorage
from datetime import datetime
# 获取日志记录器
logger = logging.getLogger(__name__)

class DataProcessor:
    """
    DataProcessor类负责处理HTML数据，解析并提取所需信息，并将结果存储到指定的存储中。

    属性:
    - soup: 用于解析HTML的BeautifulSoup对象。
    - template: 包含选择器和过滤规则的模板。
    - storage: 用于存储提取数据的存储对象。
    - queue: 存储待处理任务的队列。
    - lock: 线程锁，用于同步对队列的访问。
    - thread: 后台线程，用于处理队列中的任务。
    """

    def __init__(self,crawler,request,jobname,content, content_type, template, storage):
        """
        初始化DataProcessor对象。

        参数:
        - content: 待解析的内容（HTML或JSON）。
        - content_type: 内容类型（text/html或application/json）。
        - template: 包含选择器和过滤规则的模板。
        - storage: 用于存储提取数据的存储对象。
        """
        self.crawler = crawler
        self.request = request
        self.job_name = jobname
        self.content_type = content_type
        if content_type and 'json' in content_type.lower():
            try:
                self.data = json.loads(content)
                self.soup = None
            except json.JSONDecodeError:
                logger.error("JSON解析失败，尝试作为HTML处理")
                self.soup = BeautifulSoup(content, 'html.parser')
                self.data = None
        else:
            self.soup = BeautifulSoup(content, 'html.parser')
            self.data = None
        self.template = template
        self.storage = storage
        self.queue = asyncio.Queue()  # 使用 asyncio.Queue
        self.lock = asyncio.Lock()  # 使用 asyncio.Lock
        self.task = None  # 用于存储异步任务

    def get_attribute(self, selector, data, attr):
        """
        根据选择器和属性名获取元素的属性值。

        参数:
        - selector: CSS选择器或JSONPath表达式。
        - data: 数据源（BeautifulSoup对象或JSON数据）。
        - attr: 属性名。

        返回:
        - 属性值列表。
        """
        if self.soup:
            elements = self.soup.select(selector)
            return [element.get(attr) for element in elements if element.get(attr)]
        elif self.data:
            # 使用JSONPath处理JSON数据
            matches = jsonpath.jsonpath(self.data, selector)
            if matches:
                return [item.get(attr) if isinstance(item, dict) else None for item in matches]
        return []

    def filter(self, selector, filters):
        """
        根据过滤规则过滤选择器结果。

        参数:
        - selector: CSS选择器或JSONPath表达式。
        - filters: 过滤规则字典。

        返回:
        - 过滤后的结果列表。
        """
        # 这里可以实现各种过滤逻辑
        # 例如：文本长度过滤、正则表达式匹配等
        return []

    def get_dataBySelector(self, source, selector_config):
        """
        根据选择器配置从数据源中提取数据。

        参数:
        - source: 数据源（BeautifulSoup对象或JSON数据）。
        - selector_config: 选择器配置字典。

        返回:
        - 提取的数据字典。
        """
        result = {}
        
        for field_name, config in selector_config.items():
            if isinstance(config, str):
                # 简单选择器
                selector = config
                if self.soup:
                    elements = self.soup.select(selector)
                    result[field_name] = [element.get_text(strip=True) for element in elements]
                elif self.data:
                    matches = jsonpath.jsonpath(self.data, selector)
                    result[field_name] = matches if matches else []
            elif isinstance(config, dict):
                # 复杂选择器配置
                selector = config.get('selector', '')
                attr = config.get('attr')
                filters = config.get('filters', {})
                
                if self.soup:
                    elements = self.soup.select(selector)
                    if attr:
                        values = [element.get(attr) for element in elements if element.get(attr)]
                    else:
                        values = [element.get_text(strip=True) for element in elements]
                    
                    # 应用过滤器
                    if filters:
                        # 实现过滤逻辑
                        pass
                    
                    result[field_name] = values
                elif self.data:
                    matches = jsonpath.jsonpath(self.data, selector)
                    if matches:
                        if attr:
                            values = [item.get(attr) if isinstance(item, dict) else None for item in matches]
                            values = [v for v in values if v is not None]
                        else:
                            values = matches
                        
                        # 应用过滤器
                        if filters:
                            # 实现过滤逻辑
                            pass
                        
                        result[field_name] = values
                    else:
                        result[field_name] = []
        
        return result

    async def _process_queue(self):
        """异步处理队列中的任务"""
        while True:
            item = await self.queue.get()
            if item is None:
                break
            # 处理队列项
            self.queue.task_done()

    async def process(self):
        """
        异步处理数据并返回结果。

        返回:
        - 处理后的数据字典。
        """
        try:
            # 根据模板提取数据
            selectors = self.template.get('selectors', {})
            result = self.get_dataBySelector(self.soup or self.data, selectors)
            
            # 添加元数据
            result['_meta'] = {
                'url': self.request,
                'job_name': self.job_name,
                'timestamp': datetime.now().isoformat(),
                'content_type': self.content_type
            }
            
            # 存储数据
            if self.storage:
                await self.storage.save(result, self.job_name)
            
            return result
        except Exception as e:
            logger.error(f"数据处理失败: {str(e)}")
            return {}

    async def close(self):
        """关闭处理器并清理资源"""
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass