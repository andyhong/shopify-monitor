import json
import requests

with open("proxies.txt", "r") as proxies_txt:
    proxies_list = proxies_txt.read().split("\n")
    proxies = []
    for proxy in proxies_list:
        split = proxy.split(":")
        formatted = f"http://{split[2]}:{split[3]}@{split[0]}:{split[1]}/"
        proxies.append(formatted)

with open("config.json") as config:
    data = json.load(config)
    stores = data["stores"]
    webhook = data["webhook"]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3107.4 Safari/537.36"
}
    