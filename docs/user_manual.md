# Hermes 爬虫系统使用说明书

亲爱的用户，欢迎使用 Hermes 爬虫系统！本说明书将以通俗易懂的方式，帮助您快速上手这个强大的爬虫工具。

## 目录

- [系统是什么](#系统是什么)
- [系统怎么工作](#系统怎么工作)
- [如何开始使用](#如何开始使用)
- [如何配置系统](#如何配置系统)
- [如何设置爬虫任务](#如何设置爬虫任务)
- [如何处理数据](#如何处理数据)
- [如何存储数据](#如何存储数据)
- [如何使用API接口](#如何使用api接口)

## 系统是什么

Hermes 是一个对用户非常友好的网页数据采集工具（爬虫系统）。它就像一个智能助手，可以帮您自动收集网页上的信息，并按照您的要求整理存储。

### 它能做什么

想象一下，Hermes 就像您的私人助理，可以帮您：

- 自动收集网页上的文字、图片等信息
- 像人类一样，可以点击链接访问更多相关页面
- 按照您设定的时间表，定期更新数据
- 支持多种浏览方式（普通浏览、模拟浏览器、自动化浏览器）
- 可以把收集的数据保存成文件或存入数据库
- 提供简单的网络接口，方便您远程操控
- 允许您自定义数据的处理规则

## 系统怎么工作

让我们来看看 Hermes 的几个主要组成部分：

- 爬虫引擎（core.crawl）：负责网页数据的获取和解析
- 任务管理员（core.task）：安排和执行定时任务
- 数据处理器（core.crawl.data_processor）：整理和处理收集到的数据
- 数据管家（core.storage）：负责数据的存储工作
- 网络助手（core.web）：提供网络接口服务
- 配置中心（core.config）：管理系统的各项设置

## 如何开始使用

让我们一步一步开始使用 Hermes：

1. 首先，安装必要的工具包
```bash
pip install -r requirements.txt
```

2. 创建一个配置文件
在项目根目录创建 config.json 文件，下面是一个简单的例子：
```json
{
    "browser": {
        "chrome_path": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    },
    "storage": {
        "type": "file",
        "path": "data"
    },
    "jobs": [
        {
            "name": "我的第一个爬虫任务",
            "url": "https://example.com",
            "method": "requests",
            "template": {
                "selector": {
                    "css": ".item"  // 这里指定要采集的内容所在的区域
                },
                "attr": {
                    "标题": {  // 采集标题
                        "css": ".title",
                        "value": "@text"
                    }
                }
            }
        }
    ]
}
```

3. 启动系统
```bash
python main.py
```

## 如何配置系统

### 基础设置

配置文件就像是告诉 Hermes 要做什么的说明书。让我们来看看每个部分的含义：

```json
{
    "browser": {                 // 设置浏览器
        "chrome_path": ""      // 如果需要模拟浏览器，这里填写Chrome浏览器的安装路径
    },
    "storage": {                // 设置数据存储方式
        "type": "file",       // 可以选择存成文件(file)或使用数据库(mongodb)
        "path": "data"        // 如果选择文件存储，这里设置存储文件夹的位置
    },
    "jobs": []                 // 这里填写您要执行的爬虫任务列表
}
```

### 任务设置

每个爬虫任务的设置说明：

```json
{
    "name": "任务名称",        // 给任务起个名字
    "url": "https://example.com", // 要采集的网页地址
    "method": "requests",      // 选择访问方式：普通访问(requests)/模拟浏览器(selenium)/自动化浏览器(playwright)
    "template": {              // 设置采集规则
        "selector": {},        // 指定要采集的内容区域
        "attr": {},           // 指定要采集的具体内容
        "links": [],          // 设置是否要点击链接访问更多页面
        "filters": []         // 设置要排除的内容
    },
    "trigger_type": "interval", // 设置任务执行方式
    "trigger_args": {          // 设置执行时间
        "seconds": 3600       // 比如：每3600秒（1小时）执行一次
    }
}
```

## 如何处理数据

### 采集网页内容

下面是一个采集网页内容的例子：

```json
{
    "selector": {
        "css": ".item"         // 使用CSS选择器指定要采集的区域
    },
    "attr": {
        "标题": {             // 采集标题
            "css": ".title",  // 标题在网页中的位置
            "value": "@text"   // 获取文字内容
        },
        "链接": {             // 采集链接
            "css": "a",       // 链接的位置
            "value": "@href"   // 获取链接地址
        }
    },
    "filters": [              // 设置要排除的内容
        ".advertisement",     // 排除广告
        ".sidebar"            // 排除侧边栏
    ]
}
```

### 连续采集（点击链接）

如果您希望 Hermes 像人一样点击链接访问更多页面：

```json
{
    "links": [
        {
            "selector": "a.more-link",  // 找到要点击的链接
            "filters": [".ad-link"],    // 排除不想点击的链接
            "attr": {                   // 设置点击后要采集的内容
                "正文": {
                    "css": ".content",
                    "value": "@text"
                }
            }
        }
    ]
}
```

## 如何存储数据

### 文件存储

如果您选择将数据存储为文件：

```json
{
    "storage": {
        "type": "file",
        "path": "data"          // 数据将保存在 data 文件夹中
    }
}
```

数据将以 JSON 格式保存，每个任务会创建一个单独的文件。

### 数据库存储

如果您需要将数据存储到 MongoDB 数据库：

```json
{
    "storage": {
        "type": "mongodb",
        "host": "localhost",     // 数据库地址
        "port": 27017,           // 数据库端口
        "database": "hermes",    // 数据库名称
        "username": "",          // 用户名（可选）
        "password": ""           // 密码（可选）
    }
}
```

## 如何使用API接口

Hermes 提供了简单的网络接口，您可以通过浏览器或其他程序来控制它。

### 访问管理界面

在浏览器中访问：
```
http://localhost:8000
```

您将看到一个简单的配置界面，可以在这里设置新的爬虫任务。

### 添加新任务

您可以通过 POST 请求添加新的爬虫任务：

```bash
curl -X POST "http://localhost:8000/add_job" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "新任务",
       "url": "https://example.com",
       "method": "requests",
       "template": {
         "selector": {"css": ".item"},
         "attr": {
           "标题": {"css": ".title", "value": "@text"}
         }
       },
       "trigger_type": "interval",
       "trigger_args": {"seconds": 3600}
     }'
```

### WebSocket 实时通信

Hermes 还支持 WebSocket，可以实时获取系统状态和添加任务。

## 常见问题解答

### Q: 为什么我的爬虫不工作？

A: 请检查以下几点：
1. 网络连接是否正常
2. 目标网站是否可以访问
3. CSS 选择器是否正确
4. 查看日志文件 system.log 中的错误信息

### Q: 如何设置更复杂的采集规则？

A: 您可以：
1. 使用更精确的 CSS 选择器
2. 设置多个过滤器来排除不需要的内容
3. 使用链接采集功能来获取更深层的内容

### Q: 如何提高采集效率？

A: 建议：
1. 选择合适的采集方式（requests 最快，selenium 和 playwright 较慢但功能更强）
2. 设置合理的采集间隔，避免过于频繁的访问
3. 使用精确的 CSS 选择器，减少不必要的数据处理

## 结语

希望这份说明书能帮助您快速上手 Hermes 爬虫系统。如果您在使用过程中遇到任何问题，请查看日志文件或联系技术支持。

祝您使用愉快！
