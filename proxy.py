import requests
import random
from config import *

def test_proxies(proxies):
    working_list = []
    num_proxies = len(proxies)
    print(f"Testing {num_proxies} proxies...")
    for p in proxies:
        ps = {
            "http": p,
            "https": p
        }
        try:
            response = requests.get("https://tempcards.myshopify.com", proxies=ps, headers=headers, timeout=2)
            if response.status_code == 200:
                if response.elapsed.total_seconds() < 1:
                    working_list.append(p)
        except:
            continue
    print(f"{len(working_list)} proxies working.")
    return working_list

def get_proxy(proxies):
    index = random.randint(0, len(proxies) - 1)
    selected = {
        "http": proxies[index],
        "https": proxies[index]
    }
    return selected