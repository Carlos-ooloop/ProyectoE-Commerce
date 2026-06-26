from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.order_model import Order
from models.order_item import OrderItem
from schemas.orders import OrderCreate
from models.product_model import Product
from models.inventory_model import Inventory
from models.user_model import User


def create_order_service(db:Session, order_data : OrderCreate, user:User):
    
    order = Order(user_id = user.id,status="PENDING", total_amount = 0)
    db.add(order)
    db.flush()
    
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
    order.status = "PAID"
    try :
        db.commit()
        db.refresh(order)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500,detail="ERROR CREATING ORDER")
    return order        