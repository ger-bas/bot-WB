# from sqlalchemy import func
# from sqlalchemy.orm import sessionmaker

# from app.bot_requests.get_wb import get_product_wb
# from app.bot_utils.secondary_funcs import is_current_data
# from app.data_base.models import Product, engine

# dev
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

from bot_requests.get_wb import get_product_wb
from bot_utils.secondary_funcs import is_current_data
from data_base.models import Product, engine

session = sessionmaker(bind=engine)
s = session()


def update_product(obj: Product) -> Product:
    """Updating Product object data."""
    new_product_data = get_product_wb(obj.vendor_code)
    if not new_product_data:
        return
    obj.name = new_product_data[0]
    obj.vendor_code = new_product_data[1]
    obj.price = new_product_data[2]
    obj.rating = new_product_data[3]
    obj.quantity = new_product_data[4]
    obj.date_update = func.now()

    s.commit()
    return obj


def get_or_add_product(vendor_code: str) -> str:
    """
    Retrieves product information from the database based on the "vendor_code"
    value. If the entry is not in the database, it accesses the trading
    platform API and creates an entry in the database.
    """
    product = s.query(Product).filter_by(vendor_code=vendor_code).one_or_none()
    if product:
        if not is_current_data(product.date_update):
            new_product = update_product(product)
            if not new_product:
                return 'Этого продукта больше не существует.'
            product = new_product
        return parse_object(product)
    else:
        get_product = get_product_wb(vendor_code)
        if not get_product:
            return

        product_create = Product(
            name=get_product[0],
            vendor_code=get_product[1],
            price=get_product[2],
            rating=get_product[3],
            quantity=get_product[4]
        )
        s.add(product_create)
        s.commit()
        product = s.query(Product).filter_by(vendor_code=vendor_code).one()
        return parse_object(product)


def last_five_entries() -> list[str]:
    """Retrieves the last 5 records from the database."""
    data = s.query(Product).all()[-5:]
    return [parse_object(i) for i in data]


def parse_object(obj: Product) -> str:
    """Creates a row with product data from an object."""
    if is_current_data(obj.date_update):
        current = '✅ данные актуальны'
    else:
        current = '❌ пришлите артикул чтобы обновить данные'
    return (
        f'Название:   {obj.name}\n'
        f'Артикул:   {obj.vendor_code}\n'
        f'Цена:   {obj.price}\n'
        f'Рейтинг:   {obj.rating}\n'
        f'Количество:   {obj.quantity}\n'
        f'Актуальность:   {current}'
    )
