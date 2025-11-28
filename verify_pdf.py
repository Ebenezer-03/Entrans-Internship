import requests
import sys

def verify_pdf_generation():
    print("=== PDF GENERATION VERIFICATION START ===")
    url = "http://localhost:8000/api/pdf-report"
    
    try:
        print(f"Requesting PDF from {url}...")
        response = requests.post(url, stream=True)
        
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type')
            print(f"Response Content-Type: {content_type}")
            
            if 'application/pdf' in content_type:
                # Save to verify it's a valid file
                with open("test_report.pdf", "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print("Success: PDF file downloaded and saved as 'test_report.pdf'.")
            else:
                print(f"Error: Expected 'application/pdf', got '{content_type}'")
                sys.exit(1)
        else:
            print(f"Error: Status Code {response.status_code}")
            print(response.text)
            sys.exit(1)
            
    except Exception as e:
        print(f"Exception: {e}")
        sys.exit(1)

    print("=== PDF GENERATION VERIFICATION END ===")

if __name__ == "__main__":
    verify_pdf_generation()
