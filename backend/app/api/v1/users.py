from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_db
from app.crud.user import (
    create_user_async, get_user_async, get_users_async, update_user_async, delete_user_async
)
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.core.redis import get_redis_client
import json

router = APIRouter()

# 异步路由（性能优化）
@router.post("/", response_model=UserResponse)
async def create_new_user(user: UserCreate, db: AsyncSession = Depends(get_async_db)):
    return await create_user_async(db=db, user=user)

@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: AsyncSession = Depends(get_async_db)):
    db_user = await get_user_async(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/", response_model=list[UserResponse])
async def read_users(
    skip: int = Query(0, ge=0, le=1000, description="跳过的记录数"), 
    limit: int = Query(100, ge=10, le=1000, description="返回的记录数"), 
    db: AsyncSession = Depends(get_async_db)
):
    """获取用户列表，支持分页"""
    return await get_users_async(db=db, skip=skip, limit=limit)

@router.put("/{user_id}", response_model=UserResponse)
async def update_existing_user(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_async_db)):
    return await update_user_async(db=db, user_id=user_id, user=user)

@router.delete("/{user_id}")
async def delete_existing_user(user_id: int, db: AsyncSession = Depends(get_async_db)):
    return await delete_user_async(db=db, user_id=user_id)