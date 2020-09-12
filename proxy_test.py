import requests

url = "https://primekb.com/products.json"
proxies = {
    "http": "http://chrn_f52d!a81:6d8ff1ba@snkrs-kith-us-s467.resi.chironproxies.com:33128/",
    "https": "http://chrn_f52d!a81:6d8ff1ba@snkrs-kith-us-s467.resi.chironproxies.com:33128/"
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3107.4 Safari/537.36"
}
response = requests.get(url, proxies=proxies, headers=headers)
print(response.status_code)