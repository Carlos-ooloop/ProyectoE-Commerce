from db.data import SessionLocal
from models.user_model import User
from models.category_model import Category
from utils.auth import hash_password

def create_admin():
   db = SessionLocal()
   
   admin = db.query(User).filter(User.username == "admin").first()
   
   if not admin:
       admin = User(
                     username = "admin",
                     role = "admin",
                     email = "admin@gmail.com",
                     password = hash_password("1234"),
                    )
       db.add(admin)
       db.flush()
       db.commit()
       print("ADMIN CREATED")
   else:
       print("ADMIN ALREADY CREATED")
          
def create_categories():
    DEFAULT_CATEGORIES = ["Electrodomesticos", "Alimenticios","Aseo","Hogar"]
    db = SessionLocal()
    for category in DEFAULT_CATEGORIES:
        existing = db.query(Category).filter(Category.name == category).first()
        if existing:
            continue
        new_category = Category(name=category)
        db.add(category)
    db.commit()
    
if __name__ == "__main__":
    create_admin()
    create_categories()
        
                      