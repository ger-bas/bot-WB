from os import getenv

from dotenv import load_dotenv
from sqlalchemy import (Column, Float, ForeignKey, Integer, String,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

load_dotenv()
LOGIN = getenv('PS_LOGIN')
PASSWORD = getenv('PS_PASSWORD')
Base = declarative_base()
engine = create_engine(
    f'postgresql+psycopg2://{LOGIN}:{PASSWORD}@localhost/postgres',
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

    user_id = Column(Integer, ForeignKey('User.id'))

    def __repr__(self) -> str:
        return f'({self.id}, {self.name})'


Base.metadata.create_all(engine)
# Base.metadata.drop_all(engine)
