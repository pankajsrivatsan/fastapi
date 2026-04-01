from pydantic import BaseModel, field_validator

# for creating a product (no id needed)
class ProductCreate(BaseModel):
    name     : str
    category : str
    price    : float
    stock    : int

    @field_validator('price')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('price must be positive')
        return v

    @field_validator('stock')
    def stock_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('stock cannot be negative')
        return v

# for returning a product (id included)
class ProductResponse(BaseModel):
    id       : int
    name     : str
    category : str
    price    : float
    stock    : int

    class Config:
        from_attributes = True