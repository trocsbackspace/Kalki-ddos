import requests
import threading
import urllib3 
urllib3.disable_warnings()

# Function to send a GET request with SSL certificate verification disabled
def send_request(url):
    try:
        response = requests.get(url, verify=False)
        print(f"Response from {url}: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error sending request to {url}: {e}")

# Function to create and start threads
def send_requests_in_threads(url, num_requests):
    for _ in range(num_requests):
        t = threading.Thread(target=send_request, args=(url,))
        t.start()

if __name__ == "__main__":
    # Get URL or IP address from user input
    url_or_ip = input("Enter the URL or IP address: ")

    # Send requests using multiple threads
    while True:
        num_threads = int(input("Enter the number of threads (0 to exit): "))
        if num_threads == 0:
            break

        num_requests_per_thread = int(input("Enter the number of requests per thread: "))
        
        for _ in range(num_threads):
            send_requests_in_threads(url_or_ip, num_requests_per_thread)
