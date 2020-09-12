import requests
import time
import random
import _thread

from config import *
from db import *
from discord import *
from proxy import *

def get_product_info(product):
    product_info = {}
    product_info["id"] = product["id"]
    product_info["handle"] = product["handle"]
    product_info["title"] = product["title"]
    if len(product["images"]) > 0:
        product_info["image"] = product["images"][0]["src"]
    
    variants = []
    for variant in product["variants"]:
        variant_info = {}
        variant_info["id"] = variant["id"]
        variant_info["title"] = variant["title"]
        variant_info["price"] = variant["price"]
        variant_info["available"] = variant["available"]
        variants.append(variant_info)
    product_info["variants"] = variants
    return product_info

def init_products(stores):
    
    # Adds all current products to DB to begin monitoring
    # for new products and returns a list of IDs for each store.

    print("Adding current products...\n")
    ps = get_proxy(working_proxies)
    for store in stores:
        col = db[store]
        response = requests.get(f"https://{store}/products.json?limit=250", proxies=ps, headers=headers, timeout=3)

        if response.status_code == 200:
            print(f"Successfully retrieved products from {store}!")
        
            products_json = response.json()["products"]
            products = []
            for product in products_json:
                product_info = get_product_info(product)
                products.append(product_info)
        else:
            print(f"Could not get products for {store}! Removing from list to monitor...\n")
            stores.remove(store)
            continue
        
        
        add_products = col.insert_many(products)
        print(f"Loaded {col.count_documents({})} products for {store}.\n")
    

def query_ids(stores):
    ids = {}
    for store in stores:
        query = db[store].find({})
        id_list = []
        for q in query:
            id_list.append(q["id"])
        ids[store] = id_list
    return ids

def query_store(ids, store):
    ps = get_proxy(working_proxies)
    col = db[store]
    try:
        response = requests.get(f"https://{store}/products.json?limit=250", proxies=ps, headers=headers, timeout=3)
        products_json = response.json()["products"]
        for product in products_json:
            if product["id"] in ids[store]:
                continue
            else:
                product_info = get_product_info(product)
                send_product(webhook, store, product_info)
                col.insert_one(product_info)
        if response.elapsed.total_seconds() > 1:
            working_proxies.remove(ps["http"])
            print(f"Proxy removed from pool due to speed. {len(working_proxies)} proxies remain.")
    except:
        working_proxies.remove(ps["http"])
        print(f"Proxy removed from pool due to speed. {len(working_proxies)} proxies remain.")

def start_monitor(ids, stores):

    # Monitors stores for new products every 3 seconds and sends
    # a Discord message with ATC link if new product is found.

    print("Searching for new products...")
    start_time = time.time()
    for store in stores:
        query_store(ids, store)
    print(f"Script runtime: {round(time.time() - start_time,2)} secs")
    print("Pausing for 1 second...\n")
    time.sleep(1)

if __name__ == "__main__":
    
    init_db(db)
    working_proxies = test_proxies(proxies)
    send_alert(webhook, stores, working_proxies)
    init_products(stores)
    while True:
        ids = query_ids(stores)
        start_monitor(ids, stores)