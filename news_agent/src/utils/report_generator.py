import json
from datetime import datetime

def generate_report_payload(benchmark_results, rag_stats):
    """
    Generates a structured JSON payload that a PDF generator service would consume.
    """
    payload = {
        "metadata": {
            "title": "AI News Intelligence Comprehensive Report",
            "date": datetime.now().isoformat(),
            "author": "AI Agent"
        },
        "content": [
            {
                "type": "section",
                "title": "Executive Summary",
                "body": "This report details the performance of the AI News Intelligence System, including classification benchmarks and RAG pipeline efficiency."
            },
            {
                "type": "section",
                "title": "Classification Benchmark",
                "body": "The following table summarizes the performance of tested models:",
                "table": {
                    "headers": ["Model", "Accuracy", "F1 Score"],
                    "rows": benchmark_results # Expecting list of lists
                }
            },
            {
                "type": "section",
                "title": "RAG System Analysis",
                "body": f"The RAG system is currently indexing {rag_stats.get('doc_count', 0)} documents.",
                "metrics": rag_stats
            },
            {
                "type": "section",
                "title": "Recommendations",
                "body": "Based on the results, we recommend using DistilBERT for high-accuracy tasks and SVM for low-latency requirements."
            }
        ]
    }
    return payload
