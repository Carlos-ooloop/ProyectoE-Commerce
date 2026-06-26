from models.order_item import OrderItem
from models.order_model import Order
from utils.auth import admin_required, auth_user
from models.product_model import Product
from models.inventory_model import Inventory
from models.category_model import Category
from models.user_model import User
from models.payment_model import Payment
from fastapi import APIRouter, HTTPException, Depends
from schemas.orders import OrderCreate, OrderItemCreate
from schemas.payment import PaymentCreate
from db.data import get_db
from sqlalchemy.orm import Session
from Services.OrderServices import create_order_service
from Services.PaymentServices import process_payment
from order_crud import create_order


router = APIRouter(prefix="/payment", tags=["Payments"],dependencies=[Depends(auth_user)])


@router.post("/")
async def make_payment(payment_data:PaymentCreate,db:Session = Depends(get_db), current_user = Depends(auth_user)):
    return process_payment(db,payment_data.order_id,payment_data.client_money,current_user)
@router.get("/{id}")
async def get_payment(id:int, db:Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="PAYMENT NOT FOUND")
    return payment