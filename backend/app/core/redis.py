from typing import Optional
import redis
from app.core.config import settings

# Redis连接池
redis_pool: Optional[redis.ConnectionPool] = None

# 初始化Redis连接池
async def init_redis_pool():
    """初始化Redis连接池"""
    global redis_pool
    redis_pool = redis.ConnectionPool.from_url(
        str(settings.redis_url),
        encoding="utf-8",
        decode_responses=True,
        max_connections=100,  # 最大连接数
        socket_timeout=5.0,  # 连接超时时间
    )

# 获取Redis客户端
def get_redis_client():
    """获取Redis客户端"""
    if redis_pool is None:
        # 如果连接池未初始化，创建一个临时连接池
        return redis.Redis(
            from_url=str(settings.redis_url),
            encoding="utf-8",
            decode_responses=True,
            socket_timeout=5.0,
        )
    return redis.Redis(connection_pool=redis_pool)

# 简单的缓存装饰器，用于缓存函数结果
def cache_result(key: str, ttl: int = 3600):
    """
    缓存装饰器，用于缓存函数结果
    :param key: 缓存键前缀
    :param ttl: 缓存过期时间（秒）
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # 简化实现，暂时不使用缓存
            return await func(*args, **kwargs)
        return wrapper
    return decorator