from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import Product
from schemas import ProductCreate, ProductResponse
from typing import List
import time

Base.metadata.create_all(engine)

app = FastAPI()

# ─── CORS MIDDLEWARE ───
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # allow all origins (use specific URLs in production)
    allow_credentials=True,
    allow_methods=["*"],        # allow GET, POST, PUT, DELETE etc.
    allow_headers=["*"],        # allow all headers
)

# ─── CUSTOM MIDDLEWARE ───
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    # runs BEFORE endpoint
    print(f"→ {request.method} {request.url}")

    response = await call_next(request)  # call the actual endpoint

    # runs AFTER endpoint
    duration = time.time() - start_time
    print(f"← {response.status_code} completed in {duration:.3f}s")

    return response

# ─── YOUR ENDPOINTS (same as before) ───

def get_product_or_404(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"product with id {product_id} not found"
        )
    return product

@app.post("/products",
          response_model=ProductResponse,
          status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    existing = db.query(Product).filter(Product.name == product.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"product '{product.name}' already exists"
        )
    new_product = Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.get("/products", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no products found"
        )
    return products

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product: Product = Depends(get_product_or_404)):
    return product

@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(
    data: ProductCreate,
    product: Product = Depends(get_product_or_404),
    db: Session = Depends(get_db)
):
    product.name     = data.name
    product.category = data.category
    product.price    = data.price
    product.stock    = data.stock
    db.commit()
    db.refresh(product)
    return product

@app.delete("/products/{product_id}",
            status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product: Product = Depends(get_product_or_404),
    db: Session = Depends(get_db)
):
    db.delete(product)
    db.commit()