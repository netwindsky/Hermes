import json
import logging
from typing import Dict
from pathlib import Path

logger = logging.getLogger(__name__)
class ConfigLoader:
    """配置加载器"""
    @staticmethod
    def load_config(config_path: str = 'config/config.json') -> Dict:
        """加载配置文件"""
        try:
            # 使用Path来处理路径，确保跨平台兼容性
            base_path = Path(__file__).parent.parent.parent
            config_file = base_path / config_path
            with open(config_file, encoding='utf-8') as f:
                config = json.load(f)
                ConfigLoader._validate(config)
                return config
        except FileNotFoundError:
            logger.error(f"配置文件不存在: {config_path}")
            raise
        except json.JSONDecodeError:
            logger.error(f"配置文件格式错误: {config_path}")
            raise
            
    @staticmethod
    def _validate(config: Dict):
        """验证配置格式"""
        required_fields = ['headers', 'jobs']
        for field in required_fields:
            if field not in config:
                raise ValueError(f"缺少必要配置项: {field}")