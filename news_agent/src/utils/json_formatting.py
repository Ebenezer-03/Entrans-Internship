import json

# Color Palette
COLORS = {
    "primary": "#7B5CFF",
    "gradient_pink": "#FF50C8",
    "accent_blue": "#4B92FF",
    "sidebar_purple": "#4B3AFF",
    "background": "#F4F2FF"
}

def create_ui_response(status="success", blocks=None):
    if blocks is None:
        blocks = []
    return {
        "status": status,
        "ui_blocks": blocks
    }

def block_header(text):
    return {"type": "header", "text": text}

def block_card(title, content, footer=None):
    return {
        "type": "card", 
        "title": title, 
        "content": content,
        "footer": footer
    }

def block_metrics(items):
    """
    items: list of dicts with 'label', 'value', 'change' (optional)
    """
    return {"type": "metrics", "items": items}

def block_chat_reply(message, sender="ai"):
    return {"type": "chat_reply", "message": message, "sender": sender}

def block_rag_results(query, sources, summary, final_answer):
    return {
        "type": "rag_result",
        "query": query,
        "sources": sources,
        "summary": summary,
        "final_answer": final_answer
    }
