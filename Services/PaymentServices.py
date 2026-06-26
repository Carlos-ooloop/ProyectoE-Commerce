from sqlalchemy.orm import Session
from models.payment_model import Payment
from models.order_model import Order
from models.user_model import User
from fastapi import HTTPException
from app.enums.order_status import OrderStatus
from OrderServices import change_order_status
from app.enums.payment_status import PaymentStatus
import random
import time 
from models.inventory_model import Inventory

def fake_payment_provider(payment)->str:
    time.sleep(0.5)
    
    outcome = random.choices(population=["SUCCESS", "FAILED"], weights=[0.8,0.2], k=1)[0]
    
    return random


    
def handle_success(db, payment,order):
    payment.status = PaymentStatus.SUCCESS
    
    change_order_status(db=db, order=order,new_status=OrderStatus.PAID)
    
    db.add(payment)
    db.commit()
    db.refresh(payment)
    
    return payment



def handle_failed(db,payment,order):
    payment.status = PaymentStatus.FAILED
    for item in order.items:
        inventory = db.query(Inventory).filter(Inventory.product_id == item.product_id).with_for_update().first()
        inventory.quantity -= item.quantity
    change_order_status(db=db,order=order,new_status=OrderStatus.CANCELLED)
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment        
    
    
    
def process_payment(db:Session, order_id:int,client_money:float, user:User):
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="ORDER NOT FOUND")
    if order.user_id != user.id:
        raise HTTPException(status_code=403, detail="THIS IS NOT YOUR ORDER")
    if order.status != OrderStatus.PENDING_PAYMENT:
        raise HTTPException(status_code=400, detail="ORDER NOT PAYABLE")
    if client_money < order.total_amount:
        raise HTTPException(status_code=400, detail="NOT ENOUGH AMOUNT FOR THE ORDER")
    payment = Payment(
                      order_id = order.id,
                      amount = order.total_amount,
                      status = PaymentStatus.PENDING,
                      )
    db.add(payment)
    db.flush()
    result = fake_payment_provider(payment=payment)
    if result == "SUCCESS":
        return handle_success(db=db, payment=payment, order=order)
    return handle_failed(db=db,payment=payment,order=order)
    