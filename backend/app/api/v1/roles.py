from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db, get_async_db
from app.crud.role import (
    create_role, get_role, get_roles, update_role, delete_role,
    create_role_async, get_role_async, get_roles_async, update_role_async, delete_role_async
)
from app.schemas.role import RoleCreate, RoleUpdate, RoleResponse

router = APIRouter()

# 同步路由（保持兼容）
@router.post("/sync", response_model=RoleResponse, tags=["sync"])
def create_new_role_sync(role: RoleCreate, db: Session = Depends(get_db)):
    return create_role(db=db, role=role)

@router.get("/sync/{role_id}", response_model=RoleResponse, tags=["sync"])
def read_role_sync(role_id: int, db: Session = Depends(get_db)):
    db_role = get_role(db=db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role

@router.get("/sync", response_model=list[RoleResponse], tags=["sync"])
def read_roles_sync(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_roles(db=db, skip=skip, limit=limit)

@router.put("/sync/{role_id}", response_model=RoleResponse, tags=["sync"])
def update_existing_role_sync(role_id: int, role: RoleUpdate, db: Session = Depends(get_db)):
    return update_role(db=db, role_id=role_id, role=role)

@router.delete("/sync/{role_id}", tags=["sync"])
def delete_existing_role_sync(role_id: int, db: Session = Depends(get_db)):
    return delete_role(db=db, role_id=role_id)

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
async def read_roles(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_db)):
    return await get_roles_async(db=db, skip=skip, limit=limit)

@router.put("/{role_id}", response_model=RoleResponse)
async def update_existing_role(role_id: int, role: RoleUpdate, db: AsyncSession = Depends(get_async_db)):
    return await update_role_async(db=db, role_id=role_id, role=role)

@router.delete("/{role_id}")
async def delete_existing_role(role_id: int, db: AsyncSession = Depends(get_async_db)):
    return await delete_role_async(db=db, role_id=role_id)