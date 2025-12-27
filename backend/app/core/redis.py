import redis
from app.core.config import settings

# 创建Redis连接池
redis_pool = redis.ConnectionPool.from_url(str(settings.redis_url))

# 获取Redis客户端
def get_redis_client():
    return redis.Redis(connection_pool=redis_pool)