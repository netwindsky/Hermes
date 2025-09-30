# Hermes - 异步Web爬虫系统

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Hermes 是一个功能强大的基于Python的异步Web爬虫系统，采用模块化设计，集成了配置管理、数据存储、任务调度和Web API等功能模块，旨在实现自动化、定时化的网页抓取任务。

## ✨ 主要特性

- 🚀 **异步高性能**: 基于asyncio的异步编程，支持高并发爬取
- 🔧 **多种爬取方式**: 支持requests、selenium、playwright三种爬取方法
- ⏰ **智能任务调度**: 基于APScheduler的定时任务调度系统
- 💾 **灵活数据存储**: 支持文件存储和MongoDB存储
- 🌐 **Web API接口**: 提供RESTful API和WebSocket接口
- 🔄 **去重机制**: 使用布隆过滤器实现高效URL去重
- 🐳 **Docker支持**: 提供完整的Docker部署方案
- 📊 **实时监控**: 支持任务状态监控和日志记录

## 🏗️ 系统架构

```
Hermes/
├── core/                    # 核心功能模块
│   ├── config/             # 配置管理
│   ├── crawl/              # 爬虫核心
│   ├── storage/            # 数据存储
│   ├── task/               # 任务调度
│   └── web/                # Web API
├── config/                 # 配置文件
├── data/                   # 数据存储目录
├── docs/                   # 项目文档
├── html/                   # Web界面
├── main.py                 # 程序入口
├── docker-compose.yml      # Docker编排
└── Dockerfile             # Docker镜像
```

## 🚀 快速开始

### 环境要求

- Python 3.11+
- Docker (可选)

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置系统

编辑 `config/config.json` 文件：

```json
{
  "headers": "preset_chrome",
  "storage_type": "file",
  "request_config": {
    "verify": false,
    "timeout": 30,
    "retries": 3,
    "retry_delay": 5
  },
  "jobs": [
    {
      "name": "example_job",
      "type": "nodev",
      "method": "requests",
      "url": "https://example.com",
      "template": {
        "selector": {
          "path": "$.data[*]",
          "value": "@list"
        }
      },
      "triggerName": "every_5_seconds"
    }
  ]
}
```

### 运行系统

```bash
python main.py
```

系统启动后，Web API将在 `http://localhost:8000` 上运行。

### Docker部署

```bash
# 构建并启动
docker-compose up -d

# 查看日志
docker-compose logs -f hermes
```

## 📖 核心功能

### 1. 爬虫引擎 (WebCrawler)

- **多种爬取方式**: requests、selenium、playwright
- **异步处理**: 支持高并发爬取
- **智能去重**: 布隆过滤器避免重复爬取
- **错误重试**: 自动重试机制保证稳定性

### 2. 任务调度 (TaskScheduler)

- **定时任务**: 支持多种触发器类型
- **任务队列**: 多线程任务处理
- **状态监控**: 实时任务状态跟踪

### 3. 数据存储 (Storage)

- **文件存储**: 本地文件系统存储
- **MongoDB存储**: 支持MongoDB数据库
- **工厂模式**: 灵活切换存储方式

### 4. Web API

- **RESTful API**: 标准HTTP接口
- **WebSocket**: 实时双向通信
- **任务管理**: 动态添加和管理爬虫任务

## 🔧 技术栈

| 技术 | 用途 |
|------|------|
| Python 3.11+ | 主要编程语言 |
| FastAPI | Web框架 |
| asyncio | 异步编程 |
| APScheduler | 任务调度 |
| BeautifulSoup | HTML解析 |
| Selenium | 浏览器自动化 |
| Playwright | 现代浏览器自动化 |
| PyMongo | MongoDB驱动 |
| Docker | 容器化部署 |

## 📚 文档

- [用户手册](docs/user_manual.md) - 详细的使用说明
- [项目分析](project_analysis.md) - 系统架构分析

## 🤝 贡献

欢迎提交Issue和Pull Request来帮助改进项目！

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 [Issue](https://github.com/netwindsky/Hermes/issues)
- 发送邮件至项目维护者

---

⭐ 如果这个项目对你有帮助，请给它一个星标！