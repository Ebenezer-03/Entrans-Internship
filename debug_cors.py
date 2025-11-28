import requests

def debug_cors():
    print("=== CORS DEBUG START ===")
    url = "http://localhost:8000/api/rag-search"
    headers = {
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "content-type"
    }
    
    try:
        print(f"Sending OPTIONS request to {url}...")
        response = requests.options(url, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {response.headers}")
        
        if response.status_code == 200 and 'access-control-allow-origin' in response.headers:
            print("Success: CORS is configured correctly.")
        else:
            print("Error: CORS configuration failed.")
            
    except Exception as e:
        print(f"Exception: {e}")

    print("=== CORS DEBUG END ===")

if __name__ == "__main__":
    debug_cors()
