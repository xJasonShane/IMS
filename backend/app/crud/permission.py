from sqlmodel import Session, select
from app.models.permission import Permission
from app.schemas.permission import PermissionCreate, PermissionUpdate

def get_permission(db: Session, permission_id: int) -> Permission | None:
    return db.get(Permission, permission_id)

def get_permission_by_name(db: Session, name: str) -> Permission | None:
    statement = select(Permission).where(Permission.name == name)
    return db.exec(statement).first()

def get_permissions(db: Session, skip: int = 0, limit: int = 100) -> list[Permission]:
    statement = select(Permission).offset(skip).limit(limit)
    return db.exec(statement).all()

def create_permission(db: Session, permission: PermissionCreate) -> Permission:
    # 检查权限名称是否已存在
    existing_permission = get_permission_by_name(db, name=permission.name)
    if existing_permission:
        raise ValueError("Permission name already exists")
    
    # 创建权限对象
    db_permission = Permission(
        name=permission.name,
        description=permission.description
    )
    
    # 保存到数据库
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission

def update_permission(db: Session, permission_id: int, permission: PermissionUpdate) -> Permission:
    # 获取权限
    db_permission = get_permission(db, permission_id)
    if not db_permission:
        raise ValueError("Permission not found")
    
    # 更新权限信息
    update_data = permission.model_dump(exclude_unset=True)
    
    # 检查权限名称是否已存在
    if "name" in update_data:
        existing_permission = get_permission_by_name(db, name=update_data["name"])
        if existing_permission and existing_permission.id != permission_id:
            raise ValueError("Permission name already exists")
    
    # 更新权限对象
    for key, value in update_data.items():
        setattr(db_permission, key, value)
    
    # 保存到数据库
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission

def delete_permission(db: Session, permission_id: int) -> dict:
    # 获取权限
    db_permission = get_permission(db, permission_id)
    if not db_permission:
        raise ValueError("Permission not found")
    
    # 删除权限
    db.delete(db_permission)
    db.commit()
    
    return {"message": "Permission deleted successfully"}