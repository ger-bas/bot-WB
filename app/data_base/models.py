from os import environ

from sqlalchemy import (Column, Float, ForeignKey, Integer, String,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

POSTGRES_LOGIN = environ['POSTGRES_LOGIN']
POSTGRES_PASSWORD = environ['POSTGRES_PASSWORD']
Base = declarative_base()
engine = create_engine(
    f'postgresql+psycopg2://{POSTGRES_LOGIN}:{POSTGRES_PASSWORD}'
    '@postgres:5432/postgres',
    # echo=True
)


class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, nullable=False)
    product = relationship('Product')

    def __repr__(self) -> str:
        return f'({self.id}, {self.tg_id})'


class Product(Base):
    __tablename__ = 'Product'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    vendor_code = Column(String(20), nullable=False)
    price = Column(Float, nullable=False)
    rating = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    # date_update = ...

    user_id = Column(Integer, ForeignKey('User.id'))

    def __repr__(self) -> str:
        return f'({self.id}, {self.name})'


Base.metadata.create_all(engine)
# Base.metadata.drop_all(engine)
