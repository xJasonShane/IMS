import pytest
from sqlmodel import SQLModel, Session, create_engine
from app.core.database import get_db
from app.main import app
from fastapi.testclient import TestClient

# 创建测试数据库引擎
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# 创建测试客户端
@pytest.fixture(scope="module")
def client():
    # 创建所有表
    SQLModel.metadata.create_all(bind=engine)
    
    # 重写依赖，使用测试数据库
    def override_get_db():
        with Session(engine) as session:
            yield session
    
    app.dependency_overrides[get_db] = override_get_db
    
    yield TestClient(app)
    
    # 清理测试数据库
    SQLModel.metadata.drop_all(bind=engine)