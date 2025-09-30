import asyncio
import logging
from core import WebCrawler, TaskScheduler, StorageFactory
from core.config import ConfigLoader
from core.web.api import app
import uvicorn

# 添加项目根目录到Python路径
# sys.path.append(str(Path(__file__).parent))

async def main():
    try:
        # 配置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[logging.FileHandler('system.log'), logging.StreamHandler()]
        )

        # 加载配置
        config = ConfigLoader.load_config('config/config.json')
        if not config:
            logging.error("Failed to load configuration")
            return

        # 初始化存储
        storage_factory = StorageFactory(config)
        storage = storage_factory.create_storage()

        # 初始化爬虫和调度器
        crawler = WebCrawler(config, storage)
        scheduler = TaskScheduler(crawler, storage)  # 修改这里，传入storage参数

        # 添加任务到调度器
        for job in config.get('jobs', []):
            scheduler.add_job(job)

        # 启动调度器
        scheduler.start()

        # 初始化API模块的全局实例
        from core.web.api import init_instances
        init_instances(crawler, storage)

        # 启动FastAPI服务
        config = uvicorn.Config(app, host="0.0.0.0", port=8000)
        server = uvicorn.Server(config)
        try:
            await server.serve()
        except asyncio.CancelledError:
            logging.info("收到退出信号，正在关闭服务...")
            # 按顺序关闭各个组件
            await server.shutdown()
            scheduler.shutdown()
            await crawler.close()
            if storage:
                await storage.close()
            logging.info("所有服务已安全关闭")
            return  # 直接返回，不再执行后续代码
    except Exception as e:
        logging.error(f"程序运行时发生错误: {str(e)}")
        raise
    finally:
        # 确保所有资源都被释放
        try:
            tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
            for task in tasks:
                task.cancel()
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as e:
            logging.error(f"清理剩余任务时发生错误: {str(e)}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("收到键盘中断信号，程序正在退出...")
        # 确保在键盘中断时也能正确关闭所有资源
        try:
            # 获取当前事件循环
            loop = asyncio.get_event_loop()
            if loop and loop.is_running():
                # 取消所有正在运行的任务
                tasks = [t for t in asyncio.all_tasks(loop) if t is not asyncio.current_task()]
                for task in tasks:
                    task.cancel()
                # 等待所有任务完成
                if tasks:
                    loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
                # 关闭事件循环
                loop.close()
            logging.info("所有资源已安全关闭")
        except Exception as e:
            logging.error(f"关闭资源时发生错误: {str(e)}")
    except Exception as e:
        logging.error(f"程序异常退出: {str(e)}")