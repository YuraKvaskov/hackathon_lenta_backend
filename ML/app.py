import requests
import os
import logging
from datetime import date, timedelta
import json

# from model import forecast

current_direct = os.path.join(os.getcwd(), 'out_data') 

URL_CATEGORIES = "categories"
URL_SALES = "sales"
URL_STORES = "shops"
URL_FORECAST = "forecast"

api_port = os.environ.get("API_PORT", "8000/api/v1")
api_host = os.environ.get("API_PORT", "127.0.0.1")

_logger = logging.getLogger(__name__)


def setup_logging():
    _logger = logging.getLogger(__name__)
    _logger.setLevel(logging.DEBUG)
    handler_m = logging.StreamHandler()
    formatter_m = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
    handler_m.setFormatter(formatter_m)
    _logger.addHandler(handler_m)


def get_address(resource):
    return "http://" + api_host + ":" + api_port + "/" + resource



def write_json(val, name):
    with open(f"{name}.json", "w") as f:
        json.dump(val, f)

def get_stores():
    """ Запрос для получения списка магазинов.
    [
    {
        "st_id": "1aa057313c28fa4a40c5bc084b11d276",
        "st_city_id": "1587965fb4d4b5afe8428a4a024feb0d",
        "st_division_code": "81b4dd343f5880df806d4c5d4a846c64",
        "st_type_format_id": 4,
        "st_type_loc_id": 3,
        "st_type_size_id": 19,
        "st_is_active": false
    },
    ]
    """
    stores_url = get_address(URL_STORES)
    print(stores_url)
    resp = requests.get(stores_url)
    if resp.status_code != 200:
        _logger.warning("Could not get stores list")
        return [], resp.status_code
    return resp.json()["data"]


def get_sales(store_id=None, product_id=None):
    """
     "data": [
        {
            "store_id": "c81e728d9d4c2f636f067f89cc14862c",
            "product_id": "fe50ae64d08d4f8245aaabc55d1baf79",
            "fact": [
                {
                    "date": "2022-08-31",
                    "pr_sales_type_id": true,
                    "pr_sales_in_units": 0,
                    "pr_promo_sales_in_units": 0,
                    "pr_sales_in_rub": 61.0,
                    "pr_promo_sales_in_rub": 61.0
                },
                {
                    "date": "2023-03-14",
                    "pr_sales_type_id": false,
                    "pr_sales_in_units": 4,
                    "pr_promo_sales_in_units": 0,
                    "pr_sales_in_rub": 564.0,
                    "pr_promo_sales_in_rub": 0.0
                },
    """
    sale_url = get_address(URL_SALES)
    params = {}
    if store_id is not None:
        params["store_id"] = store_id
    if product_id is not None:
        params["product_id"] = product_id
    resp = requests.get(sale_url, params=params)
    if resp.status_code != 200:
        _logger.warning("Could not get sales history")
        return []
    return resp.json()["data"]


def get_categs_info():
    """
    {"fd064933250b0bfe4f926b867b0a5ec8":
        {
            "pr_sku_id": "fd064933250b0bfe4f926b867b0a5ec8",
            "pr_group_id": "c74d97b01eae257e44aa9d5bade97baf",
            "pr_cat_id": "1bc0249a6412ef49b07fe6f62e6dc8de",
            "pr_subcat_id": "ca34f669ae367c87f0e75dcae0f61ee5",
            "pr_uom_id": 17
        },
    }
    """
    categs_url = get_address(URL_CATEGORIES)
    resp = requests.get(categs_url)
    if resp.status_code != 200:
        _logger.warning("Could not get category info")
        return {}
    result = {el["pr_sku_id"]: el for el in resp.json()["data"]}
    return result





def main(today=date.today()):
    forecast_dates = [today + timedelta(days=d) for d in range(1, 6)]
    forecast_dates = [el.strftime("%Y-%m-%d") for el in forecast_dates]

    categs_info = get_categs_info()  # список product_id
    for store in get_stores():
        result = []
        print('store', store)
        # получаем id магазина
        store_id = store["st_id"]
        for product_id in get_categs_info():
            # получаем id продукта
            # print('store_id', store_id)
            # print('product_id', product_id)
            for item in get_sales(store_id=store_id, product_id=product_id):
                # print('item', item)
                # print('item', item["product_id"])
                # print('categs_info', categs_info)
                item_info = categs_info[item["product_id"]]
                # print('item_info', item_info)
                sales = item["fact"]
                # print('sales', sales)
                predict = (sales, item_info, store)
                print('predict\n', predict, '\n')
                # write_json(predict, name='predict')
            #     prediction = forecast(sales, item_info, store)
                
            #     result.append({"store": store["store"],
            #                 "forecast_date": today.strftime("%Y-%m-%d"),
            #                 "forecast": {"product_id": item["product_id"],
            #                                 "sales_units": {k: v for k, v in zip(forecast_dates, prediction)}
            #                                 }
            #                 })
            # requests.post(get_address(URL_FORECAST), json={"data": result})


if __name__ == "__main__":
    setup_logging()
    # stores = get_stores()
    # sales = get_sales()
    # categs_info = get_categs_info()
    # write_json(val=stores, name="stores") # работает
    # write_json(val=sales, name="sales")
    # write_json(val=categs_info, name="categs_info")
    # print(stores)
    # print(get_sales()) # не работает
    # print(get_categs_info()) #  не работает 
    main()
