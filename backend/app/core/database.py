from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool
from app.core.config import settings

# 配置数据库连接池参数
pool_kwargs = {
    "pool_size": 10,  # 连接池大小
    "max_overflow": 20,  # 最大溢出连接数
    "pool_timeout": 30,  # 连接超时时间
    "pool_recycle": 3600,  # 连接回收时间
    "echo": settings.app_debug,  # 仅在调试模式下打印SQL语句
}

# 无论使用哪种数据库，都统一使用异步引擎
if str(settings.database_url).startswith("sqlite"):
    # SQLite异步引擎配置
    engine = create_async_engine(
        str(settings.database_url.replace("sqlite://", "sqlite+aiosqlite://")),
        connect_args={"check_same_thread": False},
        **pool_kwargs
    )
else:
    # 其他数据库异步引擎配置
    engine = create_async_engine(
        str(settings.database_url),
        poolclass=AsyncAdaptedQueuePool,
        **pool_kwargs
    )

# 异步会话工厂
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,  # 提高性能，减少不必要的数据库查询
)

# 依赖函数，用于获取异步数据库会话
async def get_async_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
            await db.commit()  # 自动提交事务
        except Exception:
            await db.rollback()  # 出错时自动回滚
            raise
        finally:
            await db.close()

# 异步初始化数据库
async def async_init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)