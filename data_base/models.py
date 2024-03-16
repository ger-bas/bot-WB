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

    id = Column(Integer, primary_key=True)  # Первичный ключ.
    tg_id = Column(Integer, nullable=False)  # Telegram account id.
    product = relationship('Product')

    def __repr__(self) -> str:
        return f'({self.id}, {self.tg_id})'


class Product(Base):  # Товар
    __tablename__ = 'Product'

    id = Column(Integer, primary_key=True)  # Первичный ключ.
    name = Column(String(250), nullable=False)  # Название.
    vendor_code = Column(String(20), nullable=False)  # Артикул.
    price = Column(Float, nullable=False)  # Цена.
    rating = Column(Float, nullable=False)  # Рейтинг.
    quantity = Column(Integer, nullable=False)  # Количество(на всех складах).

    user_id = Column(Integer, ForeignKey('User.id'))  # Связь с user.

    def __repr__(self) -> str:
        return f'({self.id}, {self.name})'


Base.metadata.create_all(engine)
# Base.metadata.drop_all(engine)
