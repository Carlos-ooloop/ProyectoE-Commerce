from fastapi import APIRouter,status,HTTPException,Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from models.user_model import User
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from db.data import get_db
from sqlalchemy.orm import Session
from schemas.refresh_token import RefreshTokenRequest
from schemas.users import UserResponse
from app.core.AuditService import create_auditlog
from app.enums.audit_types import AuditAction, AuditEntity
from app.core.logging import auth_logger

router = APIRouter()
ALGORITHM = "HS256"
SECRET = "c58c87349fe778beecdd92f9cd3467d1cf0fb829b747dac15787cc44d61e3298"
oauth = OAuth2PasswordBearer(tokenUrl="/login")
TOKEN_DURATION = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def exception_not_found():
    raise HTTPException(status_code=404,detail= "USER NOT FOUND")

def password_error():
    raise HTTPException(status_code=401, detail="INCORRECT PASSWORD")

def hash_password(password:str):
   return pwd_context.hash(password)

def verify_password(normal_password:str, hashed_password:str):
    return pwd_context.verify(normal_password,hashed_password)


def create_acces_token(data:dict):
    crypt = data.copy()
    expiration = datetime.utcnow() + timedelta(minutes=TOKEN_DURATION)
    crypt.update({"exp":expiration})
    return jwt.encode(crypt,SECRET,algorithm=ALGORITHM)

def create_refresh_token(data:dict):
    crypt = data.copy()
    expiration = datetime.utcnow() + timedelta(days=7)
    crypt.update({"exp":expiration})
    return jwt.encode(crypt,SECRET,algorithm=ALGORITHM)


@router.post("/login")
async def login(form:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    
    user = db.query(User).filter(User.username == form.username).first()
    if not user:
       exception_not_found()
       
    if not verify_password(form.password,user.password):
        create_auditlog(db=db,
                        entity_type=AuditEntity.AUTH,
                        entity_id=user.id,
                        action=AuditAction.LOGIN_FAILED,
                        user_id= user.id,
                        status_after="USER_NOT_AUTENTIFIED",
                        details={"MOTIVE":"PASSWORD ERROR"}
                        )   
        password_error()
        
    access_token = create_acces_token({"sub":user.username,"role":user.role})  
    
    refresh_token = create_refresh_token({"sub":user.username,"role":user.role}) 
    
            
    return {"ACCESS TOKEN":access_token, "REFRESH TOKEN":refresh_token,"TOKEN TYPE": "BEARER"} 

@router.post("/login/auth")
async def auth_user(token:str = Depends(oauth), db:Session = Depends(get_db)):
    if not token:
        raise HTTPException(status_code=401,detail= "TO GET ACCESS TO THIS RESOURCES YOU MUST BE AUTENTIFIED")
    try:
        username = jwt.decode(token, SECRET,algorithms=ALGORITHM).get("sub")
        if username == None: 
            raise HTTPException(status_code=401, detail="THIS CREDENTIALS HAS NO VALUE")
             
    except JWTError:
            auth_logger.warning(f"USER:{username}, FAILED TO AUTH")     
            raise HTTPException(status_code=401, detail="THIS CREDENTIALS HAS NO VALUE")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        exception_not_found()
    create_auditlog(db=db,
                    entity_type=AuditEntity.AUTH,
                    entity_id=user.id,
                    action=AuditAction.LOGIN_SUCCESS,
                    user_id= user.id,
                    status_after="USER_AUTENTIFIED"
                    )    
    auth_logger.info(f"USER:{user.name}, SUCCESSFULLY AUTH")
    return user    

@router.get("/me", response_model= UserResponse)
async def me(user:User = Depends(auth_user), db:Session = Depends(get_db)):
    return db.query(User).filter(User.username == user.username).first()


async def admin_required(user:User = Depends(auth_user), db:Session = Depends(get_db)):
  if user.role != "admin":
      raise HTTPException(status_code=403,detail="YOU DONT HAVE PERMISSIONS TO THIS RESOURCES")
  return user

        
@router.put("/make-admin/{id}")
async def make_admin(id:int ,user:User = Depends(admin_required),db:Session = Depends(get_db)):
    current_user = db.query(User).filter(User.id == id).first()
    if not current_user:
        exception_not_found()
    if current_user.id == user.id:
        raise HTTPException(status_code=401,detail="YOU ARE ALREADY ADMIN")
    if current_user.role == "admin":
        raise HTTPException(status_code=401, detail="THIS USER IS ALREADY AN ADMIN")
    current_user.role = "admin"
    create_auditlog(db=db,
                    entity_type=AuditEntity.ADMIN,
                    entity_id=user.id,
                    action=AuditAction.ADMIN_PROMOTED,
                    user_id= current_user.id,
                    status_before="USER",
                    status_after="ADMIN"
                    )
    auth_logger.info(f"USER:{current_user.username}, NOW IS ADMIN. PROMOTED BY {user.username}")   
    db.commit()
    db.refresh(current_user)
    return (f"NOW {current_user.username} IS ADMIN , PROMOTED BY: {user.username}")

@router.put("/remove-admin/{id}")
async def remove_admin(id:int, user:User = Depends(admin_required), db:Session = Depends(get_db)):
    current_user = db.query(User).filter(User.id == id).first()
    if not current_user:
        exception_not_found()
    if current_user.id == user.id:
        raise HTTPException(status_code=401,detail="YOU ARE ALREADY ADMIN") 
    if current_user.role != "admin":
        raise HTTPException(status_code=401, detail="THIS USER IS NOT AN ADMIN") 
    current_user.role = "Customer"
    create_auditlog(db=db,
                    entity_type=AuditEntity.ADMIN,
                    entity_id=user.id,
                    action=AuditAction.ADMIN_REMOVED,
                    user_id= current_user.id,
                    status_before="ADMIN",
                    status_after="USER"
                    )
    auth_logger.info(f"USER:{current_user.username}, IS NO LONGER ADMIN. ROLE REMOVED BY:{user.username}")   
    db.commit()
    db.refresh(current_user)
    return (f"NOW {current_user.username} IS NO LONGER AN ADMIN , REMOVED BY: {user.username}")

@router.post("/refresh")
async def refresh(token:RefreshTokenRequest, db:Session = Depends(get_db)):
    try:
        refresh_token = jwt.decode(token.refresh_token, SECRET, algorithms=ALGORITHM)
    except JWTError:
        raise HTTPException(status_code=401, detail="THIS CREDENTIALS HAS NO VALUE")
    username = refresh_token.get("sub")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        exception_not_found()
    expiracion = datetime.utcnow() + timedelta(minutes=TOKEN_DURATION)
    new_access_token = {"sub": user.username , "exp" : expiracion}
    return {"ACCESS TOKEN": jwt.encode(new_access_token, SECRET,algorithm=ALGORITHM), "TOKEN TYPE": "BEARER"}    




    
    