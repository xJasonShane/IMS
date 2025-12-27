from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import time
from app.core.config import settings
from app.core.database import async_init_db
from app.core.redis import init_redis_pool
from app.core.logger import logger

# 创建FastAPI应用
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.app_debug,
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    # 优化JSON序列化
    json_serializer=lambda obj: obj.json(exclude_unset=True, by_alias=True),
)

# 配置GZip压缩，优化响应大小
app.add_middleware(
    GZipMiddleware,
    minimum_size=1000,  # 仅压缩大于1KB的响应
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加请求日志中间件
@app.middleware("http")
async def log_requests(request: Request, call_next):
    # 记录请求开始时间
    start_time = time.time()
    
    # 记录请求信息
    client_ip = request.client.host if request.client else "unknown"
    logger.info(
        f"Request started: {request.method} {request.url.path} from {client_ip}"
    )
    
    # 处理请求
    response = await call_next(request)
    
    # 计算响应时间
    process_time = time.time() - start_time
    
    # 记录响应信息
    logger.info(
        f"Request completed: {request.method} {request.url.path} "
        f"status_code={response.status_code} "
        f"response_time={process_time:.4f}s"
    )
    
    # 添加响应时间头
    response.headers["X-Response-Time"] = f"{process_time:.4f}s"
    
    return response

# 初始化数据库和Redis
@app.on_event("startup")
async def startup_event():
    # 初始化Redis连接池
    await init_redis_pool()
    # 初始化数据库
    await async_init_db()

# 根路由
@app.get("/")
async def read_root():
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
    }

# API版本1路由注册
from app.api.v1 import users, roles, permissions, auth, products

app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(roles.router, prefix="/api/v1/roles", tags=["roles"])
app.include_router(permissions.router, prefix="/api/v1/permissions", tags=["permissions"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(products.router, prefix="/api/v1/products", tags=["products"])