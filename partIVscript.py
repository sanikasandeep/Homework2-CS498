import requests
import time

US = "http://136.114.111.214:8080"
EU = "http://35.189.227.251:8080"

def measure_latency(url, method="GET", data=None):
    start = time.time()
    if method == "GET":
        requests.get(url)
    else:
        requests.post(url, json=data)
    end = time.time()
    return (end - start) * 1000 

def avg(arr):
    return sum(arr) / len(arr)

def test_latency():
    NUM_REQUESTS = 10

    us_register = []
    eu_register = []
    us_list = []
    eu_list = []

    for i in range(NUM_REQUESTS):
        username = f"user_{int(time.time()*1000)}_{i}"
        us_register.append(
            measure_latency(f"{US}/register", "POST", {"username": username})
        )
        eu_register.append(
            measure_latency(f"{EU}/register", "POST", {"username": username + "_eu"})
        )
        us_list.append(
            measure_latency(f"{US}/list")
        )
        eu_list.append(
            measure_latency(f"{EU}/list")
        )

    print("\n Latency Measurement:")
    print("US /register avg:", avg(us_register), "ms")
    print("EU /register avg:", avg(eu_register), "ms")
    print("US /list avg:", avg(us_list), "ms")
    print("EU /list avg:", avg(eu_list), "ms")

def test_consistency():
    misses = 0
    for i in range(100):
        username = f"consistency_{int(time.time()*1000)}_{i}"
        # POST - US
        requests.post(f"{US}/register", json={"username": username})
        # GET - EU
        response = requests.get(f"{EU}/list")
        users = response.json()["users"]
        if username not in users:
            misses += 1
    print("\n Observing Eventual Consistency:")
    print("number of times the new username was not found in the list immediately after registration:", misses)


if __name__ == "__main__":
    test_latency()
    test_consistency()