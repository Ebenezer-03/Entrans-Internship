import requests
import time
import json

def debug_rag():
    print("=== RAG DEBUG START ===")
    url = "http://localhost:8000/api/rag-search"
    payload = {"query": "What are the latest AI trends?"}
    
    start_time = time.time()
    try:
        print(f"Sending request to {url}...")
        response = requests.post(url, json=payload, timeout=30)
        end_time = time.time()
        
        duration = end_time - start_time
        print(f"Request took {duration:.2f} seconds")
        
        if response.status_code == 200:
            data = response.json()
            print("Status: Success")
            print(f"Response keys: {data.keys()}")
            if 'ui_blocks' in data:
                print(f"UI Blocks count: {len(data['ui_blocks'])}")
        else:
            print(f"Error: Status {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Exception: {e}")

    print("=== RAG DEBUG END ===")

if __name__ == "__main__":
    debug_rag()
