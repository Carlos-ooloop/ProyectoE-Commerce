from sqlalchemy.orm import Session
from models.payment_model import Payment
from models.order_model import Order
from models.user_model import User
from fastapi import HTTPException

def process_payment(db:Session, order_id:int, user:User):
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="ORDER NOT FOUND")
    if order.user_id != user.id:
        raise HTTPException(status_code=403, detail="THIS IS NOT YOUR ORDER")
    if order.status != "PENDING_PAYMENT":
        raise HTTPException(status_code=400, detail="ORDER NOT PAYABLE")
    payment = Payment(
                      order_id = order.id,
                      amount = order.total_amount,
                      status = "SUCCESS",
                      provider = "mock"
                      )
    db.add(payment)
    order.status = "PAID"
    db.commit()
    db.refresh(order)
    return payment
    