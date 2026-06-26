from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.order_model import Order
from models.order_item import OrderItem
from schemas.orders import OrderCreate
from models.product_model import Product
from models.inventory_model import Inventory
from models.user_model import User
from app.enums.order_status import OrderStatus
from app.core.AuditService import create_auditlog
from app.enums.audit_types import AuditEntity, AuditAction

ALLOWED_TRANSITIONS = {OrderStatus.PENDING_PAYMENT : {OrderStatus.PAID,OrderStatus.CANCELLED},
                       OrderStatus.PAID : {OrderStatus.SHIPPED},
                       OrderStatus.DELIVERED:set(),
                       OrderStatus.CANCELLED:set()
                       }

def change_order_status(db:Session, order:Order, new_status:OrderStatus):
    old_status = order.status
    allowed = ALLOWED_TRANSITIONS[order.status]
    if new_status not in allowed:
        raise HTTPException(status_code=400, detail=f"CANNOT CHANGE FROM {order.status} TO {new_status}")
    order.status = new_status
    create_auditlog(
                    db=db,
                    entity_type=AuditEntity.ORDER,
                    entity_id= order.id,
                    action=AuditAction.ORDER_STATUS_CHANGED,
                    user_id=order.user_id,
                    status_before=old_status,
                    status_after=new_status
                    )
    db.commit()
    db.refresh(order)
    return order



def create_order_service(db:Session, order_data : OrderCreate, user:User):
    
    order = Order(user_id = user.id,status="PENDING", total_amount = 0)
    db.add(order)
    db.flush()

    create_auditlog(db=db,
                    entity_type=AuditEntity.ORDER,
                    entity_id= order.id,
                    action=AuditAction.ORDER_CREATED,
                    user_id= user.id,
                    status_after= order.status
                    )
    
    total = 0
    order_items = []
    
    for item in order_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="PRODUCT NOT FOUND")
        
        inventory = db.query(Inventory).filter(Inventory.product_id == product.id).first()
        if inventory.quantity < item.quantity:
            raise HTTPException(status_code=400, detail="INSUFICIENT STOCK")
        
        order_item = OrderItem(
                                order_id = order.id,
                                product_id = product.id,
                                quantity = item.quantity,
                                unit_price = product.base_price
                                )
        db.add(order_item)
        order_items.append(order_item)
        inventory.quantity -= item.quantity
        total += product.base_price * item.quantity
    order.total_amount = total
    order.status = OrderStatus.PENDING_PAYMENT
    try :
        db.commit()
        db.refresh(order)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500,detail="ERROR CREATING ORDER")
    return order        