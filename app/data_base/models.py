from os import environ

from sqlalchemy import (Column, DateTime, Float, Integer, String,
                        create_engine, func)
from sqlalchemy.ext.declarative import declarative_base

POSTGRES_LOGIN = environ['POSTGRES_LOGIN']
POSTGRES_PASSWORD = environ['POSTGRES_PASSWORD']
Base = declarative_base()
engine = create_engine(
    f'postgresql+psycopg2://{POSTGRES_LOGIN}:{POSTGRES_PASSWORD}'
    '@postgres:5432/postgres',
)


class Product(Base):
    __tablename__ = 'Product'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    vendor_code = Column(String(20), nullable=False)
    price = Column(Float, nullable=False)
    rating = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    date_update = Column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f'({self.id}, {self.name})'


Base.metadata.create_all(engine)
