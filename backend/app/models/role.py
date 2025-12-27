from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

# 角色-权限关联表
class RolePermission(SQLModel, table=True):
    __tablename__ = "role_permissions"
    
    role_id: Optional[int] = Field(default=None, foreign_key="roles.id", primary_key=True, index=True)  # 外键添加索引
    permission_id: Optional[int] = Field(default=None, foreign_key="permissions.id", primary_key=True, index=True)  # 外键添加索引

class Role(SQLModel, table=True):
    __tablename__ = "roles"
    
    id: Optional[int] = Field(default=None, primary_key=True, index=True)  # 主键添加索引
    name: str = Field(index=True, unique=True, nullable=False)
    description: Optional[str] = Field(default=None)
    
    # 关联关系
    users: List["User"] = Relationship(back_populates="role")
    permissions: List["Permission"] = Relationship(back_populates="roles", link_model=RolePermission)