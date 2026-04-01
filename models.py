from sqlalchemy import String, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Product(Base):
    __tablename__ = "products"

    id       : Mapped[int]   = mapped_column(Integer, primary_key=True)
    name     : Mapped[str]   = mapped_column(String(100))
    category : Mapped[str]   = mapped_column(String(50))
    price    : Mapped[float] = mapped_column(Numeric)
    stock    : Mapped[int]   = mapped_column(Integer)