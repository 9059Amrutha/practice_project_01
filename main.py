from fastapi import Depends,FastAPI
from models import Product
from database import session, engine
import database_models

from sqlalchemy.orm import Session

database_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def greet():
    return "welcome to fastapi"


products = [
    Product(id=1, name="phone", description="budget phone", price=99, quantity=10),
    Product(id=2, name="laptop", description="budget laptop", price=999, quantity=15),
    Product(id=5, name="pen", description="budget pen", price=9, quantity=10),
    Product(id=6, name="table", description="budget table", price=18, quantity=15)
]


def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()
    



def init_db():
    db=session()
    count=db.query(database_models.Product).count

    if count==0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()
    db.close()
init_db()

@app.get("/products")
def get_all_products(db:Session = Depends(get_db)):
    db=session()

    db_products=db.query(database_models.Product).all()

    return db_products


@app.get("/product/{id}")
def get_product_by_id(id: int , db:Session = Depends(get_db)):
    db=Session()
    db_product=db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        return db_product
    return "product not found"


@app.post("/product")
def add_product(product: Product,db:Session = Depends(get_db)):
    
    db=session()
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    products.append(product)
    return product


@app.put("/product")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    
    db_product=db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "sucessfully given"
    else:
        return "no object found"





   
    


@app.delete("/product")
def delete_product(id: int,db:Session = Depends(get_db)):
    db=session()
    db_product=db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    else:
    
        return "not found"
