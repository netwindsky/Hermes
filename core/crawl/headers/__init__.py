import json
from typing import Dict
from pathlib import Path

class Headers:
    @staticmethod
    def chrome() -> Dict[str, str]:
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br"
        }
    
    @staticmethod
    def firefox() -> Dict[str, str]:
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br"
        }
    
    @staticmethod
    def edge() -> Dict[str, str]:
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br"
        }
    
    @staticmethod
    def mobile_chrome() -> Dict[str, str]:
        return {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br"
        }
    
    @staticmethod
    def mobile_safari() -> Dict[str, str]:
        return {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "Accept-Encoding": "gzip, deflate, br"
        }
    
    @staticmethod
    def _load_cookie_config() -> Dict[str, str]:
        """从配置文件加载Cookie配置"""
        try:
            config_path = Path(__file__).parent.parent.parent.parent / 'config' / 'cookies.json'
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载Cookie配置失败: {e}")
        return {}
    
    @staticmethod
    def get_headers_with_cookies(browser_type: str = 'chrome') -> Dict[str, str]:
        """获取包含Cookie的请求头"""
        headers_map = {
            'chrome': Headers.chrome(),
            'firefox': Headers.firefox(),
            'edge': Headers.edge(),
            'mobile_chrome': Headers.mobile_chrome(),
            'mobile_safari': Headers.mobile_safari()
        }
        
        headers = headers_map.get(browser_type, Headers.chrome())
        
        # 加载Cookie配置
        cookie_config = Headers._load_cookie_config()
        if cookie_config:
            # 将Cookie字典转换为Cookie字符串
            cookie_string = '; '.join([f'{k}={v}' for k, v in cookie_config.items()])
            headers['Cookie'] = cookie_string
        
        return headers
    
    @staticmethod
    def get_random_headers() -> Dict[str, str]:
        """随机获取一种浏览器的请求头"""
        import random
        browsers = ['chrome', 'firefox', 'edge', 'mobile_chrome', 'mobile_safari']
        selected_browser = random.choice(browsers)
        return Headers.get_headers_with_cookies(selected_browser)