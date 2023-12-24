import os
import requests
import time
import uuid
import random
import threading
import subprocess
from ctypes import windll
from queue import Queue

url = "https://api.discord.gx.games/v1/direct-fulfillment"
num_urls = int(input('Star https://github.com/TheCuteOwl/Discord-Nitro-Generator for making this script (If you skid, give credit ;)\nHow many nitros do you want to generate: '))

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

deleted_proxies_count = 0

def read_proxies():
    try:
        with open("proxies.txt", "r") as file:
            return file.read().splitlines()
    except:
        with open("proxies.txt", "w") as file:
            return []

def write_proxies(proxies):
    with open("proxies.txt", "w") as file:
        for proxy in proxies:
            file.write(f"{proxy}\n")

proxies = read_proxies() if use_proxies == 'yes' else [None] * num_urls

success_count = 0
lock = threading.Lock()
stop_event = threading.Event()

def generate_url(proxy):
    try:
        global success_count
        global deleted_proxies_count

        while success_count < num_urls and not stop_event.is_set():
            start_request_time = time.time()

            try:
                partner_user_id = str(uuid.uuid4())
                response = requests.post(url, json={"partnerUserId": partner_user_id}, headers=headers, proxies={"http": proxy, "https": proxy}, timeout=7)
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
                    success_count += 1
                    print(f"URL generated and saved to {output_file_path}")
                    update_window_title(success_count, len(proxies))

                    if use_proxies == 'yes' and proxy is not None:
                        create_and_start_thread(proxy)

            except requests.RequestException as e:
                if use_proxies == 'yes' and proxy is not None and isinstance(e, requests.exceptions.ProxyError) and ("WinError 10061" in str(e) or "Cannot connect to proxy." in str(e) or "TLS/SSL connection has been closed (EOF)" in str(e) or "[SSL: UNEXPECTED_EOF_WHILE_READING]" in str(e) or "Max retries exceeded with url" in str(e)) or "timed out." in str(e) or "Connection aborted" in str(e) or "Too many requests" in str(e) or "EOF occurred in violation of protocol" in str(e) or "429" in str(e):
                    proxies.remove(proxy)
                    deleted_proxies_count += 1
                    print(f"Proxy {proxy} removed from the list. Deleted Proxies: {deleted_proxies_count} - {len(proxies)} left")
                    try:
                        write_proxies(proxies)
                    except:
                        pass
                    update_window_title(success_count, len(proxies))

            end_request_time = time.time()
            request_time = end_request_time - start_request_time

    except:
        pass

def update_window_title(success_count, num_threads):
    try:
        with lock:
            window_title = f"URLs Generated: {success_count} | Working Proxies: {num_threads} | Deleted Proxies: {deleted_proxies_count}"

            if os.name == 'posix':
                subprocess.run(["printf", f"\033]0;{window_title}\007"])
            elif os.name == 'nt':
                windll.kernel32.SetConsoleTitleW(window_title)
    except:
        pass

def create_and_start_thread(proxy):
    thread = threading.Thread(target=generate_url, args=(proxy,))
    thread.start()
    return thread

def main():
    global success_count

    if use_proxies == 'no':
        while success_count < num_urls:
            generate_url(None)
    else:
        num_threads = int(input(f"Enter Number Of Threads: "))
        
        while success_count < num_urls and not stop_event.is_set():
            threads = []

            for i in range(num_threads - len(threads)):
                proxy = random.choice(proxies) if proxies else None
                thread = create_and_start_thread(proxy)
                threads.append(thread)

            for thread in threads:
                if not thread.is_alive():
                    threads.remove(thread)

            try:
                for thread in threads:
                    thread.join()
            except KeyboardInterrupt:
                print("Script terminated by user.")

            while len(threads) < num_threads and not stop_event.is_set():
                proxy = random.choice(proxies) if proxies else None
                thread = create_and_start_thread(proxy)
                threads.append(thread)

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"All URLs generated and saved! Star https://github.com/TheCuteOwl/Discord-Nitro-Generator for making this script")
        print(f"Time taken: {elapsed_time:.2f} seconds")

main()
