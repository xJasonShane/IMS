from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.models.product import Product, Warehouse, Inventory
from app.schemas.product import (
    ProductCreate, ProductUpdate,
    WarehouseCreate, WarehouseUpdate,
    InventoryCreate, InventoryUpdate
)

# 商品相关CRUD操作

async def get_product_async(db: AsyncSession, product_id: int) -> Product | None:
    """根据商品ID获取商品"""
    return await db.get(Product, product_id)

async def get_product_by_code_async(db: AsyncSession, code: str) -> Product | None:
    """根据商品编码获取商品"""
    statement = select(Product).where(Product.code == code)
    result = await db.execute(statement)
    return result.scalar_one_or_none()

async def get_products_async(db: AsyncSession, skip: int = 0, limit: int = 100) -> dict:
    """获取商品列表，支持分页"""
    # 查询商品总数
    count_statement = select(Product).count()
    count_result = await db.execute(count_statement)
    total = count_result.scalar_one()
    
    # 查询商品列表
    statement = select(Product).offset(skip).limit(limit)
    result = await db.execute(statement)
    products = result.scalars().all()
    
    # 返回包含总数和商品列表的字典
    return {
        "items": products,
        "total": total,
        "skip": skip,
        "limit": limit
    }

async def create_product_async(db: AsyncSession, product: ProductCreate) -> Product:
    """创建新商品"""
    # 检查商品编码是否已存在
    existing_product = await get_product_by_code_async(db, code=product.code)
    if existing_product:
        raise ValueError("Product code already exists")
    
    # 创建商品对象
    db_product = Product(
        name=product.name,
        code=product.code,
        description=product.description,
        category=product.category,
        unit=product.unit,
        price=product.price,
        cost=product.cost
    )
    
    # 保存到数据库
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

async def update_product_async(db: AsyncSession, product_id: int, product: ProductUpdate) -> Product:
    """更新商品信息"""
    # 获取商品
    db_product = await get_product_async(db, product_id)
    if not db_product:
        raise ValueError("Product not found")
    
    # 更新商品信息
    update_data = product.model_dump(exclude_unset=True)
    
    # 检查商品编码是否已存在
    if "code" in update_data:
        existing_product = await get_product_by_code_async(db, code=update_data["code"])
        if existing_product and existing_product.id != product_id:
            raise ValueError("Product code already exists")
    
    # 更新商品对象
    for key, value in update_data.items():
        setattr(db_product, key, value)
    
    # 保存到数据库
    await db.commit()
    await db.refresh(db_product)
    return db_product

async def delete_product_async(db: AsyncSession, product_id: int) -> dict:
    """删除商品"""
    # 获取商品
    db_product = await get_product_async(db, product_id)
    if not db_product:
        raise ValueError("Product not found")
    
    # 删除商品
    await db.delete(db_product)
    await db.commit()
    
    return {"message": "Product deleted successfully"}

# 仓库相关CRUD操作

async def get_warehouse_async(db: AsyncSession, warehouse_id: int) -> Warehouse | None:
    """根据仓库ID获取仓库"""
    return await db.get(Warehouse, warehouse_id)

async def get_warehouse_by_name_async(db: AsyncSession, name: str) -> Warehouse | None:
    """根据仓库名称获取仓库"""
    statement = select(Warehouse).where(Warehouse.name == name)
    result = await db.execute(statement)
    return result.scalar_one_or_none()

async def get_warehouses_async(db: AsyncSession, skip: int = 0, limit: int = 100) -> dict:
    """获取仓库列表，支持分页"""
    # 查询仓库总数
    count_statement = select(Warehouse).count()
    count_result = await db.execute(count_statement)
    total = count_result.scalar_one()
    
    # 查询仓库列表
    statement = select(Warehouse).offset(skip).limit(limit)
    result = await db.execute(statement)
    warehouses = result.scalars().all()
    
    # 返回包含总数和仓库列表的字典
    return {
        "items": warehouses,
        "total": total,
        "skip": skip,
        "limit": limit
    }

async def create_warehouse_async(db: AsyncSession, warehouse: WarehouseCreate) -> Warehouse:
    """创建新仓库"""
    # 检查仓库名称是否已存在
    existing_warehouse = await get_warehouse_by_name_async(db, name=warehouse.name)
    if existing_warehouse:
        raise ValueError("Warehouse name already exists")
    
    # 创建仓库对象
    db_warehouse = Warehouse(
        name=warehouse.name,
        location=warehouse.location,
        description=warehouse.description
    )
    
    # 保存到数据库
    db.add(db_warehouse)
    await db.commit()
    await db.refresh(db_warehouse)
    return db_warehouse

async def update_warehouse_async(db: AsyncSession, warehouse_id: int, warehouse: WarehouseUpdate) -> Warehouse:
    """更新仓库信息"""
    # 获取仓库
    db_warehouse = await get_warehouse_async(db, warehouse_id)
    if not db_warehouse:
        raise ValueError("Warehouse not found")
    
    # 更新仓库信息
    update_data = warehouse.model_dump(exclude_unset=True)
    
    # 检查仓库名称是否已存在
    if "name" in update_data:
        existing_warehouse = await get_warehouse_by_name_async(db, name=update_data["name"])
        if existing_warehouse and existing_warehouse.id != warehouse_id:
            raise ValueError("Warehouse name already exists")
    
    # 更新仓库对象
    for key, value in update_data.items():
        setattr(db_warehouse, key, value)
    
    # 保存到数据库
    await db.commit()
    await db.refresh(db_warehouse)
    return db_warehouse

async def delete_warehouse_async(db: AsyncSession, warehouse_id: int) -> dict:
    """删除仓库"""
    # 获取仓库
    db_warehouse = await get_warehouse_async(db, warehouse_id)
    if not db_warehouse:
        raise ValueError("Warehouse not found")
    
    # 删除仓库
    await db.delete(db_warehouse)
    await db.commit()
    
    return {"message": "Warehouse deleted successfully"}

# 库存相关CRUD操作

async def get_inventory_async(db: AsyncSession, inventory_id: int) -> Inventory | None:
    """根据库存ID获取库存"""
    return await db.get(Inventory, inventory_id)

async def get_inventory_by_product_async(db: AsyncSession, product_id: int) -> Inventory | None:
    """根据商品ID获取库存"""
    statement = select(Inventory).where(Inventory.product_id == product_id)
    result = await db.execute(statement)
    return result.scalar_one_or_none()

async def get_inventories_async(db: AsyncSession, skip: int = 0, limit: int = 100) -> dict:
    """获取库存列表，支持分页"""
    # 查询库存总数
    count_statement = select(Inventory).count()
    count_result = await db.execute(count_statement)
    total = count_result.scalar_one()
    
    # 查询库存列表，包含商品和仓库信息
    statement = select(Inventory).offset(skip).limit(limit)
    result = await db.execute(statement)
    inventories = result.scalars().all()
    
    # 返回包含总数和库存列表的字典
    return {
        "items": inventories,
        "total": total,
        "skip": skip,
        "limit": limit
    }

async def create_inventory_async(db: AsyncSession, inventory: InventoryCreate) -> Inventory:
    """创建新库存"""
    # 检查商品是否存在
    product = await get_product_async(db, inventory.product_id)
    if not product:
        raise ValueError("Product not found")
    
    # 检查仓库是否存在（如果指定了仓库）
    if inventory.warehouse_id:
        warehouse = await get_warehouse_async(db, inventory.warehouse_id)
        if not warehouse:
            raise ValueError("Warehouse not found")
    
    # 创建库存对象
    db_inventory = Inventory(
        product_id=inventory.product_id,
        quantity=inventory.quantity,
        warehouse_id=inventory.warehouse_id
    )
    
    # 保存到数据库
    db.add(db_inventory)
    await db.commit()
    await db.refresh(db_inventory)
    return db_inventory

async def update_inventory_async(db: AsyncSession, inventory_id: int, inventory: InventoryUpdate) -> Inventory:
    """更新库存信息"""
    # 获取库存
    db_inventory = await get_inventory_async(db, inventory_id)
    if not db_inventory:
        raise ValueError("Inventory not found")
    
    # 更新库存信息
    update_data = inventory.model_dump(exclude_unset=True)
    
    # 检查仓库是否存在（如果指定了仓库）
    if "warehouse_id" in update_data and update_data["warehouse_id"]:
        warehouse = await get_warehouse_async(db, update_data["warehouse_id"])
        if not warehouse:
            raise ValueError("Warehouse not found")
    
    # 更新库存对象
    for key, value in update_data.items():
        setattr(db_inventory, key, value)
    
    # 保存到数据库
    await db.commit()
    await db.refresh(db_inventory)
    return db_inventory

async def delete_inventory_async(db: AsyncSession, inventory_id: int) -> dict:
    """删除库存"""
    # 获取库存
    db_inventory = await get_inventory_async(db, inventory_id)
    if not db_inventory:
        raise ValueError("Inventory not found")
    
    # 删除库存
    await db.delete(db_inventory)
    await db.commit()
    
    return {"message": "Inventory deleted successfully"}

async def update_inventory_quantity_async(db: AsyncSession, product_id: int, quantity_change: int) -> Inventory:
    """更新商品库存数量（用于入库/出库）"""
    # 查找库存记录
    inventory = await get_inventory_by_product_async(db, product_id)
    
    if inventory:
        # 更新现有库存
        inventory.quantity += quantity_change
        if inventory.quantity < 0:
            raise ValueError("Insufficient inventory")
    else:
        # 创建新库存记录
        inventory = Inventory(
            product_id=product_id,
            quantity=quantity_change
        )
        db.add(inventory)
    
    await db.commit()
    await db.refresh(inventory)
    return inventory
