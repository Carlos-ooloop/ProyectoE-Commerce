from models.order_item import OrderItem
from models.order_model import Order
from utils.auth import admin_required, auth_user
from models.product_model import Product
from models.inventory_model import Inventory
from models.category_model import Category
from models.user_model import User
from fastapi import APIRouter, HTTPException, Depends
from schemas.orders import OrderCreate, OrderItemCreate
from db.data import get_db
from sqlalchemy.orm import Session
from Services.OrderServices import create_order_service

router = APIRouter(prefix="/orders", tags=["Orders"], dependencies=[Depends(auth_user)])

@router.post("/")
async def create_order(order_data:OrderCreate, db:Session = Depends(get_db), current_user:User = Depends(auth_user)):
   return create_order_service(db,order_data,current_user)

@router.get("/")
async def get_orders(id:int, db:Session = Depends(get_db)):
   orders = db.query(Order).all()
   return orders


@router.get("/{id}")
async def get_order(id:int, db:Session = Depends(get_db)):
   order = db.query(Order).filter(Order.id == id).first()
   if not order:
      raise HTTPException(status_code=404, detail="ORDER NOT FOUND")
   return order
