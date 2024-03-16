from .get_wb import get_product_wb
from .models import Product, User, engine
from sqlalchemy.orm import sessionmaker


def get_or_add_product(vendor_code: str, tg_user_id: int) -> Product:
    session = sessionmaker(bind=engine)
    s = session()

    try:
        print('get')
        return s.query(Product).filter_by(vendor_code=vendor_code).one()
    except Exception:
        try:
            user = s.query(User).filter_by(tg_id=tg_user_id).one()
        except Exception:
            user = User(tg_id=tg_user_id)
            s.add(user)
            s.commit()

        user = s.query(User).filter_by(tg_id=tg_user_id).one()
        product = get_product_wb(vendor_code)
        if not product:
            return

        product_create = Product(
            name=product[0],
            vendor_code=product[1],
            price=product[2],
            rating=product[3],
            quantity=product[4],
            user_id=user.id
        )
        s.add(product_create)
        s.commit()

        print('create')
        return s.query(Product).filter_by(vendor_code=vendor_code).one()


# user1 = User(tg_id=1111)
# user2 = User(tg_id=2222)

# s.add(user1)
# s.commit()

# s.add(user2)
# s.commit()

# prod1 = Product(
#     name='майка',
#     vendor_code=11111111,
#     price=12.22,
#     rating=22,
#     quantity=343,
#     user_id=1
# )
# prod2 = Product(
#     name='шорты',
#     vendor_code=22222222,
#     price=23.33,
#     rating=33,
#     quantity=454,
#     user_id=1
# )
# s.add(prod1)
# s.commit()
# s.add(prod2)
# s.commit()

# id = Column(Integer, primary_key=True)  # Первичный ключ.
# name = Column(String(250), nullable=False)  # Название.
# vendor_code = Column(Integer, nullable=False)  # Артикул.
# price = Column(Float, nullable=False)  # Цена.
# rating = Column(Integer, nullable=False)  # Рейтинг.
# quantity = Column(Integer, nullable=False)  # Количество(на всех складах).

# user = Column(Integer, ForeignKey('User.id'))

# user = s.query(User).filter_by(id=6).one()
# s.delete(user)
# s.commit()
# User.__table__.drop(engine)
# product = s.query(Product).filter_by(id=4).one()
# s.delete(product)
# s.commit()


# session = sessionmaker(bind=engine)
# s = session()
# user = s.query(User).all()
# print(user)
# product = s.query(Product).all()
# print(product)

# try:
#     ex = s.query(Product).filter_by(vendor_code=111111111).one()
#     print(ex)
# except Exception:
#     print('нет такой записи')
