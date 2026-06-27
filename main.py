from Routers import users_crud, inventory_crud, order_crud, product_crud, payments,category_crud
from fastapi import FastAPI
from utils import auth
from db.data import engine,Base
from models.user_model import User

Base.metadata.create_all(bind = engine)
app = FastAPI()

app.include_router(users_crud.router)
app.include_router(product_crud.router)
app.include_router(category_crud.router)
app.include_router(inventory_crud.router)
app.include_router(order_crud.router)
app.include_router(payments.router)
app.include_router(auth.router)
