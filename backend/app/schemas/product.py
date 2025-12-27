from sqlmodel import SQLModel
from typing import Optional

# 商品基本信息
class ProductBase(SQLModel):
    name: str
    code: str
    description: Optional[str] = None
    category: Optional[str] = None
    unit: str = "个"
    price: float = 0.0
    cost: float = 0.0

# 创建商品请求
class ProductCreate(ProductBase):
    pass

# 更新商品请求
class ProductUpdate(SQLModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    unit: Optional[str] = None
    price: Optional[float] = None
    cost: Optional[float] = None

# 商品响应
class ProductResponse(ProductBase):
    id: int
    
    class Config:
        from_attributes = True

# 仓库基本信息
class WarehouseBase(SQLModel):
    name: str
    location: Optional[str] = None
    description: Optional[str] = None

# 创建仓库请求
class WarehouseCreate(WarehouseBase):
    pass

# 更新仓库请求
class WarehouseUpdate(SQLModel):
    name: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None

# 仓库响应
class WarehouseResponse(WarehouseBase):
    id: int
    
    class Config:
        from_attributes = True

# 库存基本信息
class InventoryBase(SQLModel):
    product_id: int
    quantity: int
    warehouse_id: Optional[int] = None

# 创建库存请求
class InventoryCreate(InventoryBase):
    pass

# 更新库存请求
class InventoryUpdate(SQLModel):
    quantity: Optional[int] = None
    warehouse_id: Optional[int] = None

# 库存响应
class InventoryResponse(SQLModel):
    id: int
    product_id: int
    product: ProductResponse
    quantity: int
    warehouse_id: Optional[int] = None
    warehouse: Optional[WarehouseResponse] = None
    
    class Config:
        from_attributes = True
