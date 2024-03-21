from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from .get_wb import get_product_wb
from .models import Product, User, engine

session = sessionmaker(bind=engine)
s = session()


def save_obj(obj: object) -> None:
    """Saving an object."""
    s.add(obj)
    s.commit()


def get_or_add_product(vendor_code: str, tg_user_id: int) -> str:
    """
    Retrieves product information from the database based on the "vendor_code"
    value. If the entry is not in the database, it accesses the trading
    platform API and creates an entry in the database.
    """
    try:
        product = s.query(Product).filter_by(vendor_code=vendor_code).one()
        return parse_object(product)
    except NoResultFound:
        try:
            user = s.query(User).filter_by(tg_id=tg_user_id).one()
        except NoResultFound:
            user = User(tg_id=tg_user_id)
            save_obj(user)

        user = s.query(User).filter_by(tg_id=tg_user_id).one()
        get_product = get_product_wb(vendor_code)
        if not get_product:
            return

        product_create = Product(
            name=get_product[0],
            vendor_code=get_product[1],
            price=get_product[2],
            rating=get_product[3],
            quantity=get_product[4],
            user_id=user.id
        )
        save_obj(product_create)
        product = s.query(Product).filter_by(vendor_code=vendor_code).one()
        return parse_object(product)


def last_five_entries() -> list[str]:
    """Retrieves the last 5 records from the database."""
    data = s.query(Product).all()[-5:]
    return [parse_object(i) for i in data]


def parse_object(obj: Product) -> str:
    """Creates a row with product data from an object."""
    return (
        f'Название:   {obj.name}\n'
        f'Артикул:   {obj.vendor_code}\n'
        f'Цена:   {obj.price}\n'
        f'Рейтинг:   {obj.rating}\n'
        f'Количество:   {obj.quantity}'
    )
