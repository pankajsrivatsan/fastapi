from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import Product
from schemas import ProductCreate, ProductResponse
from typing import List

# create tables
Base.metadata.create_all(engine)

app = FastAPI()

# CREATE
@app.post("/products", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(
        name=product.name,
        category=product.category,
        price=product.price,
        stock=product.stock
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

# READ ALL
@app.get("/products", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

# READ ONE
@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="product not found")
    return product

# UPDATE
@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    existing = db.query(Product).filter(Product.id == product_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="product not found")
    existing.name     = product.name
    existing.category = product.category
    existing.price    = product.price
    existing.stock    = product.stock
    db.commit()
    db.refresh(existing)
    return existing

# DELETE
@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="product not found")
    db.delete(product)
    db.commit()
    return {"message": f"product {product_id} deleted"}