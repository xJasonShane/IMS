from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_db
from app.crud.product import (
    # 商品相关
    create_product_async, get_product_async, get_products_async, update_product_async, delete_product_async,
    # 仓库相关
    create_warehouse_async, get_warehouse_async, get_warehouses_async, update_warehouse_async, delete_warehouse_async,
    # 库存相关
    create_inventory_async, get_inventory_async, get_inventories_async, update_inventory_async, delete_inventory_async,
    update_inventory_quantity_async
)
from app.schemas.product import (
    ProductCreate, ProductUpdate, ProductResponse,
    WarehouseCreate, WarehouseUpdate, WarehouseResponse,
    InventoryCreate, InventoryUpdate, InventoryResponse
)

router = APIRouter()

# 商品相关API

@router.post("/", response_model=ProductResponse)
async def create_new_product(
    product: ProductCreate, 
    db: AsyncSession = Depends(get_async_db)
):
    """创建新商品"""
    return await create_product_async(db=db, product=product)

@router.get("/{product_id}", response_model=ProductResponse)
async def read_product(
    product_id: int, 
    db: AsyncSession = Depends(get_async_db)
):
    """根据ID获取商品"""
    product = await get_product_async(db=db, product_id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/", response_model=list[ProductResponse])
async def read_products(
    skip: int = Query(0, ge=0, le=1000, description="跳过的记录数"), 
    limit: int = Query(100, ge=10, le=1000, description="返回的记录数"), 
    db: AsyncSession = Depends(get_async_db)
):
    """获取商品列表，支持分页"""
    result = await get_products_async(db=db, skip=skip, limit=limit)
    return result["items"]

@router.put("/{product_id}", response_model=ProductResponse)
async def update_existing_product(
    product_id: int, 
    product: ProductUpdate, 
    db: AsyncSession = Depends(get_async_db)
):
    """更新商品信息"""
    return await update_product_async(db=db, product_id=product_id, product=product)

@router.delete("/{product_id}")
async def delete_existing_product(
    product_id: int, 
    db: AsyncSession = Depends(get_async_db)
):
    """删除商品"""
    return await delete_product_async(db=db, product_id=product_id)

# 仓库相关API

@router.post("/warehouses", response_model=WarehouseResponse)
async def create_new_warehouse(
    warehouse: WarehouseCreate, 
    db: AsyncSession = Depends(get_async_db)
):
    """创建新仓库"""
    return await create_warehouse_async(db=db, warehouse=warehouse)

@router.get("/warehouses/{warehouse_id}", response_model=WarehouseResponse)
async def read_warehouse(
    warehouse_id: int, 
    db: AsyncSession = Depends(get_async_db)
):
    """根据ID获取仓库"""
    warehouse = await get_warehouse_async(db=db, warehouse_id=warehouse_id)
    if warehouse is None:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    return warehouse

@router.get("/warehouses", response_model=list[WarehouseResponse])
async def read_warehouses(
    skip: int = Query(0, ge=0, le=1000, description="跳过的记录数"), 
    limit: int = Query(100, ge=10, le=1000, description="返回的记录数"), 
    db: AsyncSession = Depends(get_async_db)
):
    """获取仓库列表，支持分页"""
    result = await get_warehouses_async(db=db, skip=skip, limit=limit)
    return result["items"]

@router.put("/warehouses/{warehouse_id}", response_model=WarehouseResponse)
async def update_existing_warehouse(
    warehouse_id: int, 
    warehouse: WarehouseUpdate, 
    db: AsyncSession = Depends(get_async_db)
):
    """更新仓库信息"""
    return await update_warehouse_async(db=db, warehouse_id=warehouse_id, warehouse=warehouse)

@router.delete("/warehouses/{warehouse_id}")
async def delete_existing_warehouse(
    warehouse_id: int, 
    db: AsyncSession = Depends(get_async_db)
):
    """删除仓库"""
    return await delete_warehouse_async(db=db, warehouse_id=warehouse_id)

# 库存相关API

@router.post("/inventories", response_model=InventoryResponse)
async def create_new_inventory(
    inventory: InventoryCreate, 
    db: AsyncSession = Depends(get_async_db)
):
    """创建新库存"""
    return await create_inventory_async(db=db, inventory=inventory)

@router.get("/inventories/{inventory_id}", response_model=InventoryResponse)
async def read_inventory(
    inventory_id: int, 
    db: AsyncSession = Depends(get_async_db)
):
    """根据ID获取库存"""
    inventory = await get_inventory_async(db=db, inventory_id=inventory_id)
    if inventory is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory

@router.get("/inventories", response_model=list[InventoryResponse])
async def read_inventories(
    skip: int = Query(0, ge=0, le=1000, description="跳过的记录数"), 
    limit: int = Query(100, ge=10, le=1000, description="返回的记录数"), 
    db: AsyncSession = Depends(get_async_db)
):
    """获取库存列表，支持分页"""
    result = await get_inventories_async(db=db, skip=skip, limit=limit)
    return result["items"]

@router.put("/inventories/{inventory_id}", response_model=InventoryResponse)
async def update_existing_inventory(
    inventory_id: int, 
    inventory: InventoryUpdate, 
    db: AsyncSession = Depends(get_async_db)
):
    """更新库存信息"""
    return await update_inventory_async(db=db, inventory_id=inventory_id, inventory=inventory)

@router.delete("/inventories/{inventory_id}")
async def delete_existing_inventory(
    inventory_id: int, 
    db: AsyncSession = Depends(get_async_db)
):
    """删除库存"""
    return await delete_inventory_async(db=db, inventory_id=inventory_id)

# 库存操作API（入库/出库）

@router.put("/inventories/{product_id}/inbound", response_model=InventoryResponse)
async def inventory_inbound(
    product_id: int, 
    quantity: int = Query(..., ge=1, description="入库数量"), 
    db: AsyncSession = Depends(get_async_db)
):
    """商品入库"""
    try:
        return await update_inventory_quantity_async(db=db, product_id=product_id, quantity_change=quantity)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/inventories/{product_id}/outbound", response_model=InventoryResponse)
async def inventory_outbound(
    product_id: int, 
    quantity: int = Query(..., ge=1, description="出库数量"), 
    db: AsyncSession = Depends(get_async_db)
):
    """商品出库"""
    try:
        return await update_inventory_quantity_async(db=db, product_id=product_id, quantity_change=-quantity)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
