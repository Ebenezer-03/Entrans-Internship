import sys
import os
from fastapi.testclient import TestClient

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from news_agent.src.api.server import app

client = TestClient(app)

def verify_api():
    print("=== API VERIFICATION START ===")
    
    # 1. Health Check
    print("\n[1] Testing Health Check...")
    response = client.get("/")
    assert response.status_code == 200
    print(f"Success: {response.json()}")

    # 2. Upload Dataset
    print("\n[2] Testing Dataset Upload...")
    response = client.post("/api/upload-dataset")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "ui_blocks" in data
    print("Success: Dataset uploaded.")

    # 3. Classify
    print("\n[3] Testing Classification...")
    payload = {"text": "New AI model breaks records in speed."}
    response = client.post("/api/classify", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    # Verify UI Block structure
    assert data["ui_blocks"][0]["type"] == "chat_reply"
    assert data["ui_blocks"][1]["type"] == "card"
    print("Success: Classification response valid.")

    # 4. RAG Search
    print("\n[4] Testing RAG Search...")
    payload = {"query": "AI news"}
    response = client.post("/api/rag-search", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["ui_blocks"][1]["type"] == "rag_result"
    print("Success: RAG search response valid.")

    # 5. Summarize
    print("\n[5] Testing Summarization...")
    payload = {"text": "Long text about something..."}
    response = client.post("/api/summarize", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    print("Success: Summarization response valid.")

    # 6. Benchmark
    print("\n[6] Testing Benchmark Trigger...")
    payload = {"run_full": False}
    response = client.post("/api/benchmark", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["ui_blocks"][1]["type"] == "metrics"
    print("Success: Benchmark response valid.")

    # 7. PDF Report
    print("\n[7] Testing PDF Report Payload...")
    response = client.post("/api/pdf-report")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "Report Payload" in data["ui_blocks"][1]["title"]
    print("Success: PDF payload valid.")

    print("\n=== API VERIFICATION END: ALL TESTS PASSED ===")

if __name__ == "__main__":
    verify_api()
