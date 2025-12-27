from typing import Optional
import aioredis
from app.core.config import settings

# Redis连接池
try:
    redis_pool: Optional[aioredis.Redis] = None
except:
    redis_pool = None

# 初始化Redis连接池
async def init_redis_pool():
    """初始化Redis连接池"""
    global redis_pool
    redis_pool = aioredis.from_url(
        str(settings.redis_url),
        encoding="utf-8",
        decode_responses=True,
        max_connections=100,  # 最大连接数
        timeout=5.0,  # 连接超时时间
    )

# 获取Redis客户端
async def get_redis_client():
    """获取Redis客户端"""
    if redis_pool is None:
        await init_redis_pool()
    return redis_pool

# 缓存装饰器，用于缓存函数结果
async def cache_result(key: str, ttl: int = 3600, *, client: Optional[aioredis.Redis] = None):
    """
    缓存装饰器，用于缓存函数结果
    :param key: 缓存键前缀
    :param ttl: 缓存过期时间（秒）
    :param client: Redis客户端实例
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # 生成缓存键
            cache_key = f"{key}:{args}:{kwargs}"
            
            # 获取Redis客户端
            redis_client = client or await get_redis_client()
            
            # 尝试从缓存中获取结果
            cached_result = await redis_client.get(cache_key)
            if cached_result:
                return cached_result
            
            # 执行函数获取结果
            result = await func(*args, **kwargs)
            
            # 将结果存入缓存
            await redis_client.set(cache_key, result, ex=ttl)
            
            return result
        return wrapper
    return decorator