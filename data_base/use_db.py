from sqlalchemy.orm import sessionmaker

from .get_wb import get_product_wb
from .models import Product, User, engine


session = sessionmaker(bind=engine)
s = session()


def save_obj(obj: object) -> None:
    s.add(obj)
    s.commit()


def get_or_add_product(vendor_code: str, tg_user_id: int) -> Product:

    try:
        return s.query(Product).filter_by(vendor_code=vendor_code).one()
    except Exception:
        try:
            user = s.query(User).filter_by(tg_id=tg_user_id).one()
        except Exception:
            user = User(tg_id=tg_user_id)
            save_obj(user)

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
        save_obj(product_create)

        return s.query(Product).filter_by(vendor_code=vendor_code).one()


def last_five_entries() -> list[str]:
    data = s.query(Product).all()[-5:]
    result = [parse_object(i) for i in data]
    return result


def parse_object(_object: object) -> tuple[str]:
    ordered_object = (
        f'Название:   {_object.name}\n'
        f'Артикул:   {_object.vendor_code}\n'
        f'Цена:   {_object.price}\n'
        f'Рейтинг:   {_object.rating}\n'
        f'Количество:   {_object.quantity}'
    )
    return ordered_object
