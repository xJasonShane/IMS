from sqlmodel import Session, select
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password

def get_user(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)

def get_user_by_username(db: Session, username: str) -> User | None:
    statement = select(User).where(User.username == username)
    return db.exec(statement).first()

def get_user_by_email(db: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    return db.exec(statement).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    statement = select(User).offset(skip).limit(limit)
    return db.exec(statement).all()

def create_user(db: Session, user: UserCreate) -> User:
    # 检查用户名是否已存在
    existing_user = get_user_by_username(db, username=user.username)
    if existing_user:
        raise ValueError("Username already registered")
    
    # 检查邮箱是否已存在
    existing_email = get_user_by_email(db, email=user.email)
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
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: UserUpdate) -> User:
    # 获取用户
    db_user = get_user(db, user_id)
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
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> dict:
    # 获取用户
    db_user = get_user(db, user_id)
    if not db_user:
        raise ValueError("User not found")
    
    # 删除用户
    db.delete(db_user)
    db.commit()
    
    return {"message": "User deleted successfully"}