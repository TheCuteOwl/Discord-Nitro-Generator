# Credit me you silly 

import os
try:
    import requests
except ImportError:
    os.system("pip install requests")
import time
import requests
from concurrent.futures import ThreadPoolExecutor
import uuid
import random


url = "https://api.discord.gx.games/v1/direct-fulfillment"
num_urls = int(input('Star https://github.com/TheCuteOwl/Discord-Promo-Generator for making this script (If you skid, give credit ;)\nHow many nitro you want to generate :' ))
use_multiprocessing = input('Do you want to use multiprocessing? (yes/no): ').lower()
while use_multiprocessing not in ['yes', 'no']:
    use_multiprocessing = input('Error! Do you want to use multiprocessing? (yes/no): ').lower()

use_proxies = input('Do you want to use proxies? (yes/no): ').lower()
while use_proxies not in ['yes', 'no']:
    use_proxies = input('Error! Do you want to use proxies? (yes/no): ').lower()


headers = {
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Origin": "https://www.opera.com",
    "Referer": "https://www.opera.com/",
    "Sec-Ch-Ua": '"Opera GX";v="105", "Chromium";v="119", "Not?A_Brand";v="24"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0"
}

start_time = time.time()

def read_proxies():
    with open("proxies.txt", "r") as file:
        return file.read().splitlines()

proxies = read_proxies() if use_proxies == 'yes' else [None] * num_urls

start_time = time.time()

def generate_url(index):
    try:
        partner_user_id = str(uuid.uuid4())

        proxy = random.choice(proxies) if use_proxies == 'yes' else None

        response = requests.post(url, json={"partnerUserId": partner_user_id}, headers=headers, proxies={"http": proxy, "https": proxy})
        response.raise_for_status()

        data = response.json()
        token = data["token"]

        output_file_path = "output.txt"

        if not os.path.exists(output_file_path):
            with open(output_file_path, "w"):
                pass

        urls = 'https://discord.com/billing/partner-promotions/1180231712274387115/'
        with open(output_file_path, "a") as file:
            file.write(f"{urls}{token}\n")

        print(f"URL generated and saved to {output_file_path}")
    except requests.RequestException as e:
        print(f"Error generating URL: {e}")

        if use_proxies == 'yes' and proxy is not None and isinstance(e, requests.exceptions.ProxyError) and "WinError 10061" or "Cannot connect to proxy." or "TLS/SSL connection has been closed (EOF)" in str(e):
            proxies.remove(proxy)
            print(f"Proxy {proxy} removed from the list.")

if use_multiprocessing == 'yes':
    with ThreadPoolExecutor() as executor:
        executor.map(generate_url, range(num_urls))
else:
    for i in range(num_urls):
        generate_url(i)

if use_multiprocessing == 'yes':
    with ThreadPoolExecutor() as executor:
        executor.map(generate_url, range(num_urls))
else:
    for i in range(num_urls):
        generate_url(i)
end_time = time.time()

elapsed_time = end_time - start_time
print(f"All URLs generated and saved! Star https://github.com/TheCuteOwl/Discord-Promo-Generator for making this script")
print(f"Time taken: {elapsed_time:.2f} seconds")
