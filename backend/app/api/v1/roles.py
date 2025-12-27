from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.database import get_db
from app.crud.role import create_role, get_role, get_roles, update_role, delete_role
from app.schemas.role import RoleCreate, RoleUpdate, RoleResponse

router = APIRouter()

@router.post("/", response_model=RoleResponse)
def create_new_role(role: RoleCreate, db: Session = Depends(get_db)):
    return create_role(db=db, role=role)

@router.get("/{role_id}", response_model=RoleResponse)
def read_role(role_id: int, db: Session = Depends(get_db)):
    db_role = get_role(db=db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role

@router.get("/", response_model=list[RoleResponse])
def read_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_roles(db=db, skip=skip, limit=limit)

@router.put("/{role_id}", response_model=RoleResponse)
def update_existing_role(role_id: int, role: RoleUpdate, db: Session = Depends(get_db)):
    return update_role(db=db, role_id=role_id, role=role)

@router.delete("/{role_id}")
def delete_existing_role(role_id: int, db: Session = Depends(get_db)):
    return delete_role(db=db, role_id=role_id)