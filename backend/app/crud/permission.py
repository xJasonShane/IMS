from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.permission import Permission
from app.schemas.permission import PermissionCreate, PermissionUpdate

# 异步操作
async def get_permission_async(db: AsyncSession, permission_id: int) -> Permission | None:
    """根据权限ID获取权限"""
    return await db.get(Permission, permission_id)

async def get_permission_by_name_async(db: AsyncSession, name: str) -> Permission | None:
    """根据权限名称获取权限"""
    statement = select(Permission).where(Permission.name == name)
    result = await db.execute(statement)
    return result.scalar_one_or_none()

async def get_permissions_async(db: AsyncSession, skip: int = 0, limit: int = 100) -> dict:
    """获取权限列表，支持分页"""
    # 查询权限总数
    count_statement = select(Permission).count()
    count_result = await db.execute(count_statement)
    total = count_result.scalar_one()
    
    # 查询权限列表
    statement = select(Permission).offset(skip).limit(limit)
    result = await db.execute(statement)
    permissions = result.scalars().all()
    
    # 返回包含总数和权限列表的字典
    return {
        "items": permissions,
        "total": total,
        "skip": skip,
        "limit": limit
    }

async def create_permission_async(db: AsyncSession, permission: PermissionCreate) -> Permission:
    """创建新权限"""
    # 检查权限名称是否已存在
    existing_permission = await get_permission_by_name_async(db, name=permission.name)
    if existing_permission:
        raise ValueError("Permission name already exists")
    
    # 创建权限对象
    db_permission = Permission(
        name=permission.name,
        description=permission.description
    )
    
    # 保存到数据库
    db.add(db_permission)
    await db.commit()
    await db.refresh(db_permission)
    return db_permission

async def update_permission_async(db: AsyncSession, permission_id: int, permission: PermissionUpdate) -> Permission:
    """更新权限信息"""
    # 获取权限
    db_permission = await get_permission_async(db, permission_id)
    if not db_permission:
        raise ValueError("Permission not found")
    
    # 更新权限信息
    update_data = permission.model_dump(exclude_unset=True)
    
    # 检查权限名称是否已存在
    if "name" in update_data:
        existing_permission = await get_permission_by_name_async(db, name=update_data["name"])
        if existing_permission and existing_permission.id != permission_id:
            raise ValueError("Permission name already exists")
    
    # 更新权限对象
    for key, value in update_data.items():
        setattr(db_permission, key, value)
    
    # 保存到数据库
    await db.commit()
    await db.refresh(db_permission)
    return db_permission

async def delete_permission_async(db: AsyncSession, permission_id: int) -> dict:
    """删除权限"""
    # 获取权限
    db_permission = await get_permission_async(db, permission_id)
    if not db_permission:
        raise ValueError("Permission not found")
    
    # 删除权限
    await db.delete(db_permission)
    await db.commit()
    
    return {"message": "Permission deleted successfully"}