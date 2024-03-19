import requests


def get_product_wb(vendor_code: str) -> tuple:
    """
    Obtaining information about a product by article number
     from the WB website.
    """
    url = ('https://card.wb.ru/cards/v1/detail?appType=1'
           '&curr=rub&dest=-1257786&spp=30&nm=')
    response = requests.get(url + vendor_code)

    products = response.json()['data']['products']
    if not products:
        return

    product = products[0]

    name = product['name']

    id = product['id']

    price = str(product["salePriceU"])
    price = float(f'{price[:-2]}.{price[-2:]}')

    rating = product['reviewRating']

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
