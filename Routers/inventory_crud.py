from fastapi import APIRouter, status, HTTPException,Depends
from utils.auth import admin_required, auth_user
from db.data import get_db
from sqlalchemy.orm import Session
from models.product_model import Product
from models.category_model import Category
from models.inventory_model import Inventory
from schemas.product import ProductCreate,ProductResponse,ProductUpdate
from schemas.inventory import InventoryAdjust
from datetime import datetime

router = APIRouter(prefix="/inventory", tags=["Inventory"])


@router.get("/{product_id}", dependencies=[Depends(admin_required)])
async def get_inventory(product_id:int ,db:Session=Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id==product_id).first()
    if not inventory:
        raise HTTPException(status_code=404,detail="INVENTORY NOT FOUND")
    return inventory


@router.patch("/{product_id}/adjust", dependencies=[Depends(admin_required)])
async def act_inventory(product_id:int,inventory:InventoryAdjust, db:Session=Depends(get_db)):
    existing_inventory = db.query(Inventory).filter(Inventory.product_id == product_id).first()
    if not existing_inventory:
        raise HTTPException(status_code=404,detail="INVENTORY NOT FOUND")
    new_quantity = existing_inventory.quantity + inventory.quantity
    if new_quantity < 0:
        raise HTTPException(status_code=400, detail="INSUFICIENT STOCK")
    existing_inventory.quantity = new_quantity
    db.commit()
    db.refresh(existing_inventory)
    return existing_inventory      

