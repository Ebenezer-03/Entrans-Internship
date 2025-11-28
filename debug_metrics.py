import requests
import time

def debug_metrics():
    print("=== METRICS DEBUG START ===")
    url = "http://localhost:8000/api/metrics"
    
    start_time = time.time()
    try:
        print(f"Sending request to {url}...")
        response = requests.post(url, timeout=10)
        end_time = time.time()
        
        duration = end_time - start_time
        print(f"Request took {duration:.2f} seconds")
        
        if response.status_code == 200:
            print("Status: Success")
            print(response.json())
        else:
            print(f"Error: Status {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Exception: {e}")

    print("=== METRICS DEBUG END ===")

if __name__ == "__main__":
    debug_metrics()
