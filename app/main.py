from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from .routes import router

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# 创建 FastAPI 应用实例
app = FastAPI(
    title="Runtime-py-core API",
    description="工作流运行时 API 服务",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI 路径
    redoc_url="/redoc",  # ReDoc 路径
    openapi_url="/openapi.json",  # OpenAPI 规范路径
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)

# 注册路由
app.include_router(router)

# 健康检查端点
@app.get("/health", tags=["health"])
async def health_check():
    """
    健康检查端点
    
    返回服务器状态
    """
    return {"status": "ok"}


@app.get("/", tags=["root"])
async def root():
    """
    根路径重定向到 API 文档
    """
    return {"message": "Welcome to Runtime-py-core API. Visit /api/docs for Swagger documentation."}