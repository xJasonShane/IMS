from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_db
from app.crud.permission import (
    create_permission_async, get_permission_async, get_permissions_async, update_permission_async, delete_permission_async
)
from app.schemas.permission import PermissionCreate, PermissionUpdate, PermissionResponse

router = APIRouter()

# 异步路由（性能优化）
@router.post("/", response_model=PermissionResponse)
async def create_new_permission(permission: PermissionCreate, db: AsyncSession = Depends(get_async_db)):
    return await create_permission_async(db=db, permission=permission)

@router.get("/{permission_id}", response_model=PermissionResponse)
async def read_permission(permission_id: int, db: AsyncSession = Depends(get_async_db)):
    db_permission = await get_permission_async(db=db, permission_id=permission_id)
    if db_permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")
    return db_permission

@router.get("/", response_model=list[PermissionResponse])
async def read_permissions(
    skip: int = Query(0, ge=0, le=1000, description="跳过的记录数"), 
    limit: int = Query(100, ge=10, le=1000, description="返回的记录数"), 
    db: AsyncSession = Depends(get_async_db)
):
    """获取权限列表，支持分页"""
    result = await get_permissions_async(db=db, skip=skip, limit=limit)
    return result["items"]

@router.put("/{permission_id}", response_model=PermissionResponse)
async def update_existing_permission(permission_id: int, permission: PermissionUpdate, db: AsyncSession = Depends(get_async_db)):
    return await update_permission_async(db=db, permission_id=permission_id, permission=permission)

@router.delete("/{permission_id}")
async def delete_existing_permission(permission_id: int, db: AsyncSession = Depends(get_async_db)):
    return await delete_permission_async(db=db, permission_id=permission_id)