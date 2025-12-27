from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# 创建数据库引擎
# SQLite需要添加check_same_thread=False参数
if str(settings.database_url).startswith("sqlite"):
    engine = create_engine(
        str(settings.database_url),
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(str(settings.database_url))

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 依赖函数，用于获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 初始化数据库
def init_db():
    # 创建所有表
    SQLModel.metadata.create_all(engine)