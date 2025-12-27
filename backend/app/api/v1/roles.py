from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_db
from app.crud.role import (
    create_role_async, get_role_async, get_roles_async, update_role_async, delete_role_async
)
from app.schemas.role import RoleCreate, RoleUpdate, RoleResponse

router = APIRouter()

# 异步路由（性能优化）
@router.post("/", response_model=RoleResponse)
async def create_new_role(role: RoleCreate, db: AsyncSession = Depends(get_async_db)):
    return await create_role_async(db=db, role=role)

@router.get("/{role_id}", response_model=RoleResponse)
async def read_role(role_id: int, db: AsyncSession = Depends(get_async_db)):
    db_role = await get_role_async(db=db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role

@router.get("/", response_model=list[RoleResponse])
async def read_roles(
    skip: int = Query(0, ge=0, le=1000, description="跳过的记录数"), 
    limit: int = Query(100, ge=10, le=1000, description="返回的记录数"), 
    db: AsyncSession = Depends(get_async_db)
):
    """获取角色列表，支持分页"""
    result = await get_roles_async(db=db, skip=skip, limit=limit)
    return result["items"]

@router.put("/{role_id}", response_model=RoleResponse)
async def update_existing_role(role_id: int, role: RoleUpdate, db: AsyncSession = Depends(get_async_db)):
    return await update_role_async(db=db, role_id=role_id, role=role)

@router.delete("/{role_id}")
async def delete_existing_role(role_id: int, db: AsyncSession = Depends(get_async_db)):
    return await delete_role_async(db=db, role_id=role_id)