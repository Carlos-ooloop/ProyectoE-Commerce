from db.data import get_db
from models.user_model import User
from utils.auth import admin_required, auth_user, hash_password,exception_not_found
from schemas.users import UserCreate, UserResponse,UserUpdate
from jose import JWTError, jwt
from fastapi import APIRouter, HTTPException,status,Depends
from sqlalchemy.orm import Session
from app.core.AuditService import create_auditlog
from app.enums.audit_types import AuditAction,AuditEntity
from app.core.logging import user_logger

router = APIRouter(prefix="/users", tags=["Users"])

def already_exists():
    raise HTTPException(status_code=400, detail="USER ALREADY EXISTS")


@router.post("/register",response_model=UserResponse)
async def register(user:UserCreate, db:Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        already_exists()
    user.password = hash_password(user.password)
    new_user = User(username = user.username,
                    password = user.password,
                    email = user.email)
    db.add(new_user)
    db.flush()
    create_auditlog(db=db,
                    entity_type=AuditEntity.USER,
                    entity_id=new_user.id,
                    action=AuditAction.USER_CREATED,
                    user_id= new_user.id,
                    status_before="NONE",
                    status_after="REGISTERED"
                    ) 
    user_logger.info(f"USER : {new_user.username}, SUCCESFULLY REGISTERED")
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/", response_model= list[UserResponse], dependencies=[Depends(auth_user)])
async def get_all(db:Session = Depends(get_db)):
    return db.query(User).all()


@router.get("/{id}", response_model= UserResponse, dependencies=[Depends(auth_user)])
async def get_by_id(id:int, db:Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        exception_not_found()
    return user    



@router.put("/{id}", response_model=UserResponse, dependencies=[Depends(admin_required)])
async def user_update(id:int, current_user:UserUpdate, db:Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.id == id).first()
    if not existing_user:
        exception_not_found()
    if existing_user.username is not None:
        existing_user.username = current_user.username
    if existing_user.email is not None:
        existing_user.email = current_user.email
    if existing_user.password is not None:
        existing_user.password = hash_password(current_user.password)   
          
    db.commit()
    db.refresh(existing_user)
    return existing_user




@router.delete("/{id}", dependencies=[Depends(admin_required)])
async def delete_user(id:int, db:Session = Depends(get_db), admin_user:User = Depends(admin_required)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        exception_not_found()
    db.delete(user)
    create_auditlog(db=db,
                    entity_type=AuditEntity.USER,
                    entity_id=user.id,
                    action=AuditAction.USER_ELIMINATED,
                    user_id= user.id,
                    status_before="IN_DB",
                    status_after="ELIMINATED"
                    )
    user_logger.info(f"USER: {user.username}, SUCCESFULLY DELETED BY: {admin_user.username}")   
    db.commit()

    return (f"USER {user.username} DELETED SUCCESSFULLY ")    





