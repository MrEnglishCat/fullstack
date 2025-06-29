from sqlalchemy import String, Float, Integer, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, sessionmaker
from sqlalchemy.testing.schema import mapped_column


class Base(DeclarativeBase):
    ...

class ProductCard(Base):

    __tablename__ = 'product_card'

    id: Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[int] = mapped_column(String(255))
    price:Mapped[float] = mapped_column(Float)
    sale_price:Mapped[float] = mapped_column(Float)
    rating:Mapped[float] = mapped_column(Float)
    review_count:Mapped[int] = mapped_column(Integer)




engine = create_engine('sqlite:///parser/data/products.db', echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(engine)

