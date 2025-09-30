# crawler.py
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import json
from urllib.parse import urlparse, urljoin
from typing import Dict, Optional, List, Set, Tuple
from pybloom_live import ScalableBloomFilter
from playwright.async_api import async_playwright
import asyncio
from core.crawl.data_processor import DataProcessor  # 修改为绝对导入
from core.crawl.headers import Headers
# 确保 logger 被正确导入
logger = logging.getLogger(__name__)

class WebCrawler:
    """支持多层级页面抓取的爬虫核心类"""

    def __init__(self, config: Dict, storage):
        self.config = config
        self.job_configs = {}
        self.storage = storage  # 传递存储实例
        self.bloom_filters = {}
        self._init_job_settings()
        self.drivers = {}  # 先初始化为空字典
        self.session = requests.Session()  # 创建一个Session对象
        adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        self.semaphore = asyncio.Semaphore(10)  # 控制并发度为10
        #self.data_processor = DataProcessor(storage)  # 初始化 DataProcessor

    def _init_job_settings(self):
        """从配置初始化各job的爬取参数"""
        for job in self.config.get('jobs', []):
            # 初始化布隆过滤器
            bf = ScalableBloomFilter(
                initial_capacity=job.get('bloomfilter', {}).get('capacity', 10000),
                error_rate=job.get('bloomfilter', {}).get('error_rate', 0.001)
            )
            self.bloom_filters[job['name']] = bf
            # 缓存job配置
            self.job_configs[job['name']] = job

    async def initialize(self):  # 新增异步初始化方法
        """异步初始化驱动"""
        self.drivers = await self.async_init_drivers()

    async def async_init_drivers(self) -> Dict:  # 改为异步方法
        """异步初始化浏览器驱动"""
        drivers = {
            'selenium': None,
            'playwright': None,
            'browser': None
        }
        try:
            # 从配置中获取浏览器路径，如果未配置则使用默认值
            chrome_path = self.config.get('browser', {}).get('chrome_path')
            # 配置Selenium Chrome选项
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')  # 启用无头模式
            chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
            if chrome_path:
                chrome_options.binary_location = chrome_path
            
            # 初始化Selenium Chrome驱动
            drivers['selenium'] = webdriver.Chrome(options=chrome_options)
            
            # 使用 async with 管理生命周期
            async with async_playwright() as playwright:
                drivers['playwright'] = playwright
                # 配置Playwright浏览器选项
                browser = await playwright.chromium.launch(
                    headless=True,  # 启用无头模式
                    executable_path=chrome_path if chrome_path else None  # 如果配置了路径则使用
                )
                drivers['browser'] = browser
        except Exception as e:
            logger.error(f"浏览器驱动初始化失败: {str(e)}")
        return drivers
    async def process_url(self, url: str, job_name: str, current_depth: int = 0) -> Tuple[Dict, List[str]]:
        """
        处理一个URL并返回抓取结果及子链接
        :param url: 目标URL
        :param job_name: 任务名称
        :param current_depth: 当前爬取深度
        :return: (数据结果, 新发现的链接列表)
        """
        # 初始化返回结果
        result = {}
        new_links = []
        try:
            job_config = self.job_configs.get(job_name)
            if not job_config:
                logger.error(f"job_config 未找到: {job_name}")
                return result, new_links
            template = job_config.get('template', {})  # 修改: 使用 get 方法避免 KeyError
            if not template:
                logger.error(f"job_config 缺少 'template' 键: {job_name}")
                return result, new_links
            # 获取页面内容
            html, content_type = await self.fetch(url, job_config.get('method', 'requests'))
            if not html:
                logger.warning(f"无法获取页面内容: {url}")
                return result, new_links
            # 处理数据
            processor = DataProcessor(self, url, job_name, html, content_type, template, self.storage)
            result = await processor.process()
            # 如果需要爬取子链接且未达到最大深度
            max_depth = job_config.get('max_depth', 1)
            if current_depth < max_depth:
                # 提取子链接
                links_config = template.get('links', {})
                if links_config:
                    soup = BeautifulSoup(html, 'html.parser')
                    link_elements = soup.select(links_config.get('selector', 'a[href]'))
                    for element in link_elements:
                        href = element.get('href')
                        if href:
                            # 转换为绝对URL
                            absolute_url = urljoin(url, href)
                            # 检查是否已经爬取过
                            if absolute_url not in self.bloom_filters[job_name]:
                                self.bloom_filters[job_name].add(absolute_url)
                                new_links.append(absolute_url)
        except Exception as e:
            logger.error(f"处理URL时发生错误 {url}: {str(e)}")
        return result, new_links
    async def fetch(self, url: str, method: str = 'requests') -> Tuple[Optional[str], Optional[str]]:
        """
        获取页面内容
        :param url: 目标URL
        :param method: 抓取方法 ('requests', 'selenium', 'playwright')
        :return: (页面内容, 内容类型)
        """
        try:
            if method == 'requests':
                async with self.semaphore:
                    headers = self.config.get('headers', {})
                    response = self.session.get(url, headers=headers, timeout=30)
                    response.raise_for_status()
                    content_type = response.headers.get('content-type', '')
                    return response.text, content_type
            elif method == 'selenium':
                if not self.drivers.get('selenium'):
                    logger.error("Selenium驱动未初始化")
                    return None, None
                async with self.semaphore:
                    self.drivers['selenium'].get(url)
                    html = self.drivers['selenium'].page_source
                    return html, 'text/html'
            elif method == 'playwright':
                if not self.drivers.get('browser'):
                    logger.error("Playwright浏览器未初始化")
                    return None, None
                async with self.semaphore:
                    page = await self.drivers['browser'].new_page()
                    try:
                        await page.goto(url)
                        html = await page.content()
                        return html, 'text/html'
                    finally:
                        await page.close()
            else:
                logger.error(f"不支持的抓取方法: {method}")
                return None, None
        except Exception as e:
            logger.error(f"获取页面内容失败 {url}: {str(e)}")
            return None, None
    def parse(self, html: str, selectors: Dict) -> Dict:
        """
        解析HTML内容
        :param html: HTML内容
        :param selectors: 选择器配置
        :return: 解析结果
        """
        soup = BeautifulSoup(html, 'html.parser')
        result = {}
        for key, selector in selectors.items():
            elements = soup.select(selector)
            result[key] = [element.get_text(strip=True) for element in elements]
        return result
    async def close(self):
        """关闭所有驱动实例"""
        try:
            if self.drivers.get('selenium'):
                self.drivers['selenium'].quit()
            if self.drivers.get('browser'):
                await self.drivers['browser'].close()
            if self.session:
                self.session.close()
        except Exception as e:
            logger.error(f"关闭驱动实例时发生错误: {str(e)}")