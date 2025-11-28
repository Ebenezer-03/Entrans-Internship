import sys

# Color Constants
PRIMARY_GRADIENT_START = "#7B5CFF"
PRIMARY_GRADIENT_END = "#FF50C8"
SIDEBAR_BG = "#4B3AFF"
CHAT_BUBBLE_USER = "#7B5CFF"
CHAT_BUBBLE_AI = "#4B92FF"
BG_COLOR = "#F4F2FF"

def print_card(title, content, style="default"):
    """
    Prints a card-style block.
    Since we are in a terminal/text environment, we simulate cards with borders and headers.
    """
    border = "═" * 60
    print(f"\n{border}")
    print(f"  {title.upper()}  ")
    print(f"{border}")
    if isinstance(content, list):
        for item in content:
            print(f"• {item}")
    elif isinstance(content, dict):
        for k, v in content.items():
            print(f"• {k}: {v}")
    else:
        print(content)
    print(f"{border}\n")

def print_header(text):
    print(f"\n\n{'='*40}")
    print(f" {text.upper()} ")
    print(f"{'='*40}\n")

def format_classification_result(model_name, metrics):
    """
    Formats classification metrics into a nice table/card.
    metrics: dict with accuracy, precision, recall, f1
    """
    content = {
        "Model": model_name,
        "Accuracy": f"{metrics.get('accuracy', 0):.4f}",
        "Precision": f"{metrics.get('precision', 0):.4f}",
        "Recall": f"{metrics.get('recall', 0):.4f}",
        "F1 Score": f"{metrics.get('f1', 0):.4f}"
    }
    print_card(f"Model Performance: {model_name}", content)

def format_rag_response(query, retrieved_items, summary, final_answer):
    print_header("RAG RESPONSE")
    
    print_card("Query", query)
    
    # Top Sources
    sources = []
    for item in retrieved_items[:3]:
        sources.append(f"{item['source']} (Score: {item['score']:.2f})")
    print_card("Top Sources", sources)
    
    print_card("Summary", summary)
    
    print_card("Final Answer", final_answer)

def print_neon_separator():
    print("\n" + "~" * 40 + "\n")
