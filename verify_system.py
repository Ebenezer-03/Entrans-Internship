import sys
import os

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'news_agent'))
print(f"DEBUG: sys.path: {sys.path}")
try:
    import src
    print(f"DEBUG: src imported from {src.__file__}")
except ImportError as e:
    print(f"DEBUG: Failed to import src: {e}")

from src.utils.data_loader import load_zenodo_dataset, preprocess_data
from src.classification.benchmark import run_benchmark
from src.rag.rag_engine import RAGEngine

def verify():
    print("=== VERIFICATION START ===")
    
    # 1. Test Data Loading
    print("\n[1] Testing Data Loader...")
    df = load_zenodo_dataset()
    df = preprocess_data(df)
    print(f"Data loaded: {len(df)} rows")
    
    # 2. Test Benchmark
    print("\n[2] Testing Classification Benchmark...")
    try:
        run_benchmark()
        print("Benchmark completed successfully.")
    except Exception as e:
        print(f"Benchmark FAILED: {e}")
        import traceback
        traceback.print_exc()
        
    # 3. Test RAG
    print("\n[3] Testing RAG Engine...")
    try:
        rag = RAGEngine()
        rag.ingest_data(df.head(20)) # Ingest small subset
        rag.process_query("What is the news about AI?")
        print("RAG query processed successfully.")
    except Exception as e:
        print(f"RAG FAILED: {e}")
        import traceback
        traceback.print_exc()

    print("\n=== VERIFICATION END ===")

if __name__ == "__main__":
    verify()
