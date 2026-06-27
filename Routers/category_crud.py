from fastapi import APIRouter, status, HTTPException,Depends
from utils.auth import admin_required, auth_user
from db.data import get_db
from sqlalchemy.orm import Session
from models.product_model import Product
from models.category_model import Category
from models.inventory_model import Inventory
from datetime import datetime
from schemas.categories import CategoryCreate, CategoryResponse,CategoryUpdate
from app.core.AuditService import create_auditlog
from app.enums.audit_types import AuditAction, AuditEntity
from app.core.logging import category_logger


router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=CategoryResponse, dependencies=[Depends(admin_required)])
async def create_category(new_category:CategoryCreate, db:Session = Depends(get_db)):
    existing_category = db.query(Category).filter(Category.name == new_category.name).first()
    if existing_category:
        raise HTTPException(status_code=400, detail="THIS CATEGORY ALREADY EXISTS")
    category = Category(name = new_category.name,
                        parent_id = new_category.parent_id)
    db.add(category)
    create_auditlog(db=db,
                    entity_type=AuditEntity.CATEGORY,
                    entity_id=category.id,
                    action=AuditAction.CATEGORY_CREATED,
                    user_id= category.id,
                    status_before="NONE",
                    status_after="CREATED"
                    )
    category_logger.info(f"CATEGORY:{category.name}, WAS CREATED SUCCESSFULLY  ")  
    db.commit()
    db.refresh(category)
    return category


@router.get("/", response_model=list[CategoryResponse], dependencies=[Depends(auth_user)])
async def get_all(db:Session = Depends(get_db)):
    categories = db.query(Category).all()
    return categories



@router.put("/{id}", response_model=CategoryResponse, dependencies=[Depends(admin_required)])
async def act_category(id:int, act_category:CategoryUpdate,db:Session = Depends(get_db)):
    existing_category = db.query(Category).filter(Category.id == id).first()
    if not existing_category:
        raise HTTPException(status_code=404,detail="CATEGORY NOT FOUND")
    update = act_category.model_dump(exclude_unset=True)
    for key,value in update.items():
        setattr(existing_category,key,value)
    category_logger.info(f"CATEGORY:{existing_category.name}, MODIFIED ")    
    db.commit()
    db.refresh(existing_category)   

@router.delete("/{id}", dependencies=[Depends(admin_required)])
async def delete_category(id:int, db:Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == id).first()
    if not category:
        raise HTTPException(status_code=404,detail="CATEGORY NOT FOUND")
    products = db.query(Product).filter(Product.category_id == category.id).first()
    if products:
        raise HTTPException(status_code=400,detail="CATEGORY CONTAIN PRODUCTS")
    db.delete(category)
    create_auditlog(db=db,
                    entity_type=AuditEntity.CATEGORY,
                    entity_id=category.id,
                    action=AuditAction.CATEGORY_ELIMINATED,
                    user_id= category.id,
                    status_before="IN_DB",
                    status_after="ELIMINATED"
                    )  
    category_logger.info(f"CATEGORY: {category.name}, DELETED")
    db.commit()
    return (f"CATEGORY: {category.name}, DELETED SUCCESSFULLY ")