import requests
import urllib3 
import random
import concurrent.futures

# Disable SSL certificate verification warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Function to send a GET request with SSL certificate verification disabled
def send_request(url):
    try:
        headers = {'User-Agent': generate_user_agent()}
        response = requests.get(url, headers=headers, verify=False)
        print(f"Response from {url}: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error sending request to {url}: {e}")

# Function to generate a random User-Agent
def generate_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        # Add more user agents as needed
    ]
    return random.choice(user_agents)

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
        except FileNotFoundError:
            print("Proxy file not found.")
            exit()

    # Send requests using multiple threads
    while True:
        num_threads = int(input("Enter the number of threads (0 to exit): "))
        if num_threads == 0:
            break

        num_requests_per_thread = int(input("Enter the number of requests per thread: "))

        # Create a thread pool executor
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            # Submit requests to the executor
            for _ in range(num_threads):
                executor.submit(send_request, url_or_ip)
