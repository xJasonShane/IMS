from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password

# 异步操作
async def get_user_async(db: AsyncSession, user_id: int) -> User | None:
    """根据用户ID获取用户"""
    return await db.get(User, user_id)

async def get_user_by_username_async(db: AsyncSession, username: str) -> User | None:
    """根据用户名获取用户"""
    statement = select(User).where(User.username == username)
    result = await db.execute(statement)
    return result.scalar_one_or_none()

async def get_user_by_email_async(db: AsyncSession, email: str) -> User | None:
    """根据邮箱获取用户"""
    statement = select(User).where(User.email == email)
    result = await db.execute(statement)
    return result.scalar_one_or_none()

async def get_users_async(db: AsyncSession, skip: int = 0, limit: int = 100) -> dict:
    """获取用户列表，支持分页"""
    # 查询用户总数
    count_statement = select(User).count()
    count_result = await db.execute(count_statement)
    total = count_result.scalar_one()
    
    # 查询用户列表
    statement = select(User).offset(skip).limit(limit)
    result = await db.execute(statement)
    users = result.scalars().all()
    
    # 返回包含总数和用户列表的字典
    return {
        "items": users,
        "total": total,
        "skip": skip,
        "limit": limit
    }

async def create_user_async(db: AsyncSession, user: UserCreate) -> User:
    """创建新用户"""
    # 检查用户名是否已存在
    existing_user = await get_user_by_username_async(db, username=user.username)
    if existing_user:
        raise ValueError("Username already registered")
    
    # 检查邮箱是否已存在
    existing_email = await get_user_by_email_async(db, email=user.email)
    if existing_email:
        raise ValueError("Email already registered")
    
    # 创建用户对象
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        password=hashed_password,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        role_id=user.role_id
    )
    
    # 保存到数据库
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def update_user_async(db: AsyncSession, user_id: int, user: UserUpdate) -> User:
    """更新用户信息"""
    # 获取用户
    db_user = await get_user_async(db, user_id)
    if not db_user:
        raise ValueError("User not found")
    
    # 更新用户信息
    update_data = user.model_dump(exclude_unset=True)
    
    # 如果更新密码，需要重新加密
    if "password" in update_data:
        update_data["password"] = get_password_hash(update_data["password"])
    
    # 更新用户对象
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    # 保存到数据库
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def delete_user_async(db: AsyncSession, user_id: int) -> dict:
    """删除用户"""
    # 获取用户
    db_user = await get_user_async(db, user_id)
    if not db_user:
        raise ValueError("User not found")
    
    # 删除用户
    await db.delete(db_user)
    await db.commit()
    
    return {"message": "User deleted successfully"}