from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from typing import List
from app.models.role import Role, RolePermission
from app.models.permission import Permission
from app.schemas.role import RoleCreate, RoleUpdate

# 异步操作
async def get_role_async(db: AsyncSession, role_id: int) -> Role | None:
    """根据角色ID获取角色"""
    return await db.get(Role, role_id)

async def get_role_by_name_async(db: AsyncSession, name: str) -> Role | None:
    """根据角色名称获取角色"""
    statement = select(Role).where(Role.name == name)
    result = await db.execute(statement)
    return result.scalar_one_or_none()

async def get_roles_async(db: AsyncSession, skip: int = 0, limit: int = 100) -> dict:
    """获取角色列表，支持分页"""
    # 查询角色总数
    count_statement = select(Role).count()
    count_result = await db.execute(count_statement)
    total = count_result.scalar_one()
    
    # 查询角色列表
    statement = select(Role).offset(skip).limit(limit)
    result = await db.execute(statement)
    roles = result.scalars().all()
    
    # 返回包含总数和角色列表的字典
    return {
        "items": roles,
        "total": total,
        "skip": skip,
        "limit": limit
    }

async def create_role_async(db: AsyncSession, role: RoleCreate) -> Role:
    """创建新角色"""
    # 检查角色名称是否已存在
    existing_role = await get_role_by_name_async(db, name=role.name)
    if existing_role:
        raise ValueError("Role name already exists")
    
    # 创建角色对象
    db_role = Role(
        name=role.name,
        description=role.description
    )
    
    # 保存到数据库
    db.add(db_role)
    await db.commit()
    await db.refresh(db_role)
    
    # 关联权限
    if role.permission_ids:
        # 获取所有权限
        permissions = await db.execute(
            select(Permission).where(Permission.id.in_(role.permission_ids))
        )
        permissions = permissions.scalars().all()
        
        # 创建关联关系
        for permission in permissions:
            role_permission = RolePermission(role_id=db_role.id, permission_id=permission.id)
            db.add(role_permission)
        
        await db.commit()
        await db.refresh(db_role)
    
    return db_role

async def update_role_async(db: AsyncSession, role_id: int, role: RoleUpdate) -> Role:
    """更新角色信息"""
    # 获取角色
    db_role = await get_role_async(db, role_id)
    if not db_role:
        raise ValueError("Role not found")
    
    # 更新角色信息
    update_data = role.model_dump(exclude_unset=True)
    
    # 更新角色基本信息
    if "name" in update_data:
        # 检查角色名称是否已存在
        existing_role = await get_role_by_name_async(db, name=update_data["name"])
        if existing_role and existing_role.id != role_id:
            raise ValueError("Role name already exists")
        db_role.name = update_data["name"]
    
    if "description" in update_data:
        db_role.description = update_data["description"]
    
    # 更新角色权限关联
    if "permission_ids" in update_data:
        # 删除现有关联
        await db.execute(delete(RolePermission).where(RolePermission.role_id == role_id))
        
        # 创建新关联
        if update_data["permission_ids"]:
            permissions = await db.execute(
                select(Permission).where(Permission.id.in_(update_data["permission_ids"]))
            )
            permissions = permissions.scalars().all()
            
            for permission in permissions:
                role_permission = RolePermission(role_id=role_id, permission_id=permission.id)
                db.add(role_permission)
    
    # 保存到数据库
    await db.commit()
    await db.refresh(db_role)
    return db_role

async def delete_role_async(db: AsyncSession, role_id: int) -> dict:
    """删除角色"""
    # 获取角色
    db_role = await get_role_async(db, role_id)
    if not db_role:
        raise ValueError("Role not found")
    
    # 删除角色权限关联
    await db.execute(delete(RolePermission).where(RolePermission.role_id == role_id))
    
    # 删除角色
    await db.delete(db_role)
    await db.commit()
    
    return {"message": "Role deleted successfully"}