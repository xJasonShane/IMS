from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from app.models.role import RolePermission

class Permission(SQLModel, table=True):
    __tablename__ = "permissions"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)
    description: Optional[str] = Field(default=None)
    
    # 关联关系
    roles: List["Role"] = Relationship(back_populates="permissions", link_model=RolePermission)