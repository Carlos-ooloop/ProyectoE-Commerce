from fastapi import APIRouter, status, HTTPException,Depends
from utils.auth import admin_required, auth_user
from db.data import get_db
from sqlalchemy.orm import Session
from models.product_model import Product
from models.category_model import Category
from models.inventory_model import Inventory
from schemas.product import ProductCreate,ProductResponse,ProductUpdate
from datetime import datetime
from app.core.AuditService import create_auditlog
from app.enums.audit_types import AuditAction,AuditEntity


allowed_fields_in_products = {
                              "name",
                              "description",
                              "brand",
                              "category_id",
                              "base_price",
                              "unit",
                              "characteristics"
                              }

def already_exists():
    raise HTTPException(status_code=400, detail="THIS PRODUCT ALREADY EXISTS")
def exception_not_found():
    raise HTTPException(status_code=404, detail="PRODUCT DOESNT EXISTS")



router = APIRouter( prefix="/products", tags=["Products"], dependencies=[Depends(auth_user)])



@router.post("/", response_model=ProductResponse,dependencies=[Depends(admin_required)])
async def add_product(new_product : ProductCreate, db:Session = Depends(get_db)):
    
    existing_product = db.query(Product).filter(Product.name == new_product.name, Product.brand == new_product.brand).first()
    
    if existing_product:
        already_exists()
        
    product = Product(
                      name =new_product.name,
                      brand = new_product.brand,
                      description = new_product.description,
                      category_id = new_product.category_id,
                      base_price = new_product.base_price,
                      unit = new_product.unit,
                      characteristics = new_product.characteristics
                      )   
    db.add(product)
    db.flush()
    
    inventory = Inventory(product_id = product.id, quantity = 0)
    db.add(inventory)
    create_auditlog(db=db,
                    entity_type=AuditEntity.PRODUCT,
                    entity_id=product.id,
                    action=AuditAction.PRODUCT_CREATED,
                    user_id= product.id,
                    status_before="NONE",
                    status_after="CREATED"
                    )   
    db.commit()
    db.refresh(product)
    
    return product 

@router.get("/", response_model=list[ProductResponse], dependencies=[Depends(auth_user)])
async def get_all_products(db:Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

@router.put("/{id}", response_model=ProductResponse,dependencies = [Depends(admin_required)])
async def act_product(id:int, act_product = ProductUpdate,db:Session = Depends(get_db)):
    
    existing_product = db.query(Product).filter(Product.id == id).first()
    if not existing_product:
        exception_not_found()
    update = act_product.model_dump(exclude_unset=True)
    if "category_id" in update:
        category = db.query(Category).filter(Category.id == update["category_id"]).first()
        if not category:
            raise HTTPException(status_code=404, detail="CATEGORY NOT FOUND")
    
    for key,value in update.items():
        if key in allowed_fields_in_products:
         setattr(existing_product,key,value)
    db.commit()
    db.refresh(existing_product)
    return existing_product 

@router.delete("/{id}", dependencies=[Depends(admin_required)])
async def delete_product(id:int, db:Session = Depends(get_db)):
    existing_product = db.query(Product).filter(Product.id == id).first()
    if not existing_product:
        exception_not_found()
    existing_product.deleted_at = datetime.utcnow()
    create_auditlog(db=db,
                    entity_type=AuditEntity.PRODUCT,
                    entity_id=existing_product.id,
                    action=AuditAction.PRODUCT_ELIMINATED,
                    user_id= existing_product.id,
                    status_before="IN_DB",
                    status_after="DELETED"
                    )  
    db.commit()
    db.refresh(existing_product)
    return (f"PRODUCT : {existing_product.name}, DELETED SUCCESSFULLY")


    
            
    








