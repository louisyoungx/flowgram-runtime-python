import uvicorn
import logging
import os
import sys
import asyncio

# 添加当前目录到 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def main():
    logger.info("FlowGram Python Runtime")
    logger.info("API server: http://0.0.0.0:4000")
    logger.info("Swagger UI: http://0.0.0.0:4000/docs")
    logger.info("ReDoc: http://0.0.0.0:4000/redoc")
    
    # 启动 uvicorn 服务器
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",  # 监听所有网络接口
        port=4000,       # 在端口 4000 上运行
        reload=True,     # 启用热重载（开发模式）
        log_level="info",
    )

if __name__ == "__main__":
    # 确保有事件循环可用
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())
    
    main()
