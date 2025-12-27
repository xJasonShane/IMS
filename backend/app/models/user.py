from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True, index=True)  # 主键添加索引
    username: str = Field(index=True, unique=True, nullable=False)
    password: str = Field(nullable=False)
    email: str = Field(index=True, unique=True, nullable=False)
    full_name: Optional[str] = Field(default=None, index=True)  # 姓名添加索引
    is_active: bool = Field(default=True, index=True)  # 活跃状态添加索引
    is_superuser: bool = Field(default=False, index=True)  # 超级用户状态添加索引
    
    # 关联关系
    role_id: Optional[int] = Field(default=None, foreign_key="roles.id", index=True)  # 外键添加索引
    role: Optional["Role"] = Relationship(back_populates="users")