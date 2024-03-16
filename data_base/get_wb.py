import requests

# vendor = '15398364'
# vendor = '131108268'


def get_product_wb(vendor_code: str) -> tuple:
    """
    Obtaining information about a product by article number
     from the WB website.
    """
    url = ('https://card.wb.ru/cards/v1/detail?appType=1'
           '&curr=rub&dest=-1257786&spp=30&nm=')
    response = requests.get(url + vendor_code)

    # Обьект товара.
    products = response.json()['data']['products']
    if not products:
        return

    product = products[0]

    # Название товара.
    name = product['name']

    # Артикул.
    id = product['id']

    # Цена со скидкой.
    price = str(product["salePriceU"])
    price = float(f'{price[:-2]}.{price[-2:]}')

    # Рейтинг по отзывам.
    rating = product['reviewRating']

    # Количество товара на всех складах.
    sizes = product['sizes']
    quantity = 0
    for item in sizes:
        stocks = item['stocks']
        if stocks:
            for i in stocks:
                quantity += i['qty']
        else:
            break

    return name, id, price, rating, quantity


# print(get_product_wb(vendor))
