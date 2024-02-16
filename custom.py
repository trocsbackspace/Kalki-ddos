import requests
import threading
from random import choice
import urllib3 
urllib3.disable_warnings()

# Function to send a GET request with SSL certificate verification disabled
def send_request(session, url, proxy=None):
    try:
        if proxy:
            response = session.get(url, proxies={'http': proxy, 'https': proxy}, verify=False)
        else:
            response = session.get(url, verify=False)
        print(f"Response from {url} using proxy {proxy}: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error sending request to {url} using proxy {proxy}: {e}")

# Function to create and start threads
def send_requests_in_threads(url, num_requests, proxies=None):
    # Create a session object to reuse the connection
    session = requests.Session()
    for _ in range(num_requests):
        proxy = choice(proxies) if proxies else None
        t = threading.Thread(target=send_request, args=(session, url, proxy))
        t.start()

# Function to filter working proxies from the given list
def filter_working_proxies(proxies):
    working_proxies = []
    for proxy in proxies:
        try:
            response = requests.get("https://www.google.com", proxies={'http': proxy, 'https': proxy}, timeout=5)
            if response.status_code == 200:
                working_proxies.append(proxy)
        except requests.RequestException:
            pass
    return working_proxies

if __name__ == "__main__":
    # Get URL or IP address from user input
    url_or_ip = input("Enter the URL or IP address: ")

    # Get proxy file name from user input
    proxy_file = input("Enter the proxy file name (write 0 if not using proxies): ")

    # Read proxies from file if provided
    proxies = None
    if proxy_file != "0":
        try:
            with open(proxy_file, "r") as file:
                proxies = file.read().splitlines()
            proxies = filter_working_proxies(proxies)
        except FileNotFoundError:
            print("Proxy file not found.")
            exit()

    # Send requests using multiple threads
    while True:
        num_threads = int(input("Enter the number of threads (0 to exit): "))
        if num_threads == 0:
            break

        num_requests_per_thread = int(input("Enter the number of requests per thread: "))

        # If proxies are provided, use them
        if proxies:
            send_requests_in_threads(url_or_ip, num_requests_per_thread, proxies)
        else:
            send_requests_in_threads(url_or_ip, num_requests_per_thread)
