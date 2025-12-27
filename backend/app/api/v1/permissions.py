from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.database import get_db
from app.crud.permission import create_permission, get_permission, get_permissions, update_permission, delete_permission
from app.schemas.permission import PermissionCreate, PermissionUpdate, PermissionResponse

router = APIRouter()

@router.post("/", response_model=PermissionResponse)
def create_new_permission(permission: PermissionCreate, db: Session = Depends(get_db)):
    return create_permission(db=db, permission=permission)

@router.get("/{permission_id}", response_model=PermissionResponse)
def read_permission(permission_id: int, db: Session = Depends(get_db)):
    db_permission = get_permission(db=db, permission_id=permission_id)
    if db_permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")
    return db_permission

@router.get("/", response_model=list[PermissionResponse])
def read_permissions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_permissions(db=db, skip=skip, limit=limit)

@router.put("/{permission_id}", response_model=PermissionResponse)
def update_existing_permission(permission_id: int, permission: PermissionUpdate, db: Session = Depends(get_db)):
    return update_permission(db=db, permission_id=permission_id, permission=permission)

@router.delete("/{permission_id}")
def delete_existing_permission(permission_id: int, db: Session = Depends(get_db)):
    return delete_permission(db=db, permission_id=permission_id)