from typing import Optional, Any
from pydantic_settings import BaseSettings
from pydantic import RedisDsn

class Settings(BaseSettings):
    # 应用配置
    app_name: str = "IMS"
    app_version: str = "1.0.0"
    app_debug: bool = True
    
    # 数据库配置
    database_url: Any
    
    # Redis配置
    redis_url: RedisDsn
    
    # JWT配置
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS配置
    backend_cors_origins: list[str] = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()