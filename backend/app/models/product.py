from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Product(SQLModel, table=True):
    __tablename__ = "products"
    
    id: Optional[int] = Field(default=None, primary_key=True, index=True)  # 主键添加索引
    name: str = Field(index=True, unique=True, nullable=False)  # 商品名称
    code: str = Field(index=True, unique=True, nullable=False)  # 商品编码
    description: Optional[str] = Field(default=None)  # 商品描述
    category: Optional[str] = Field(default=None, index=True)  # 商品类别
    unit: str = Field(default="个")  # 商品单位
    price: float = Field(default=0.0)  # 商品价格
    cost: float = Field(default=0.0)  # 商品成本
    
    # 关联关系
    inventory: Optional["Inventory"] = Relationship(back_populates="product")

class Inventory(SQLModel, table=True):
    __tablename__ = "inventories"
    
    id: Optional[int] = Field(default=None, primary_key=True, index=True)  # 主键添加索引
    product_id: int = Field(foreign_key="products.id", index=True)  # 商品ID，外键添加索引
    quantity: int = Field(default=0)  # 库存数量
    warehouse_id: Optional[int] = Field(default=None, foreign_key="warehouses.id", index=True)  # 仓库ID，外键添加索引
    
    # 关联关系
    product: Optional[Product] = Relationship(back_populates="inventory")
    warehouse: Optional["Warehouse"] = Relationship(back_populates="inventories")

class Warehouse(SQLModel, table=True):
    __tablename__ = "warehouses"
    
    id: Optional[int] = Field(default=None, primary_key=True, index=True)  # 主键添加索引
    name: str = Field(index=True, unique=True, nullable=False)  # 仓库名称
    location: Optional[str] = Field(default=None)  # 仓库位置
    description: Optional[str] = Field(default=None)  # 仓库描述
    
    # 关联关系
    inventories: List[Inventory] = Relationship(back_populates="warehouse")
