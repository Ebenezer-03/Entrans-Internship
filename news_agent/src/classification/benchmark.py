import pandas as pd
from src.utils.data_loader import load_zenodo_dataset, preprocess_data
from src.classification.traditional import TraditionalClassifier
from src.classification.nlu import NLUClassifier
from src.classification.llm import LLMClassifier
from src.utils.formatting import format_classification_result, print_card, print_header, print_neon_separator

def run_benchmark():
    print_header("Starting Classification Benchmark")
    
    # 1. Load Data
    print("Loading dataset...")
    df = load_zenodo_dataset()
    df = preprocess_data(df)
    print(f"Dataset loaded: {len(df)} records.")
    
    all_results = {}
    
    # 2. Traditional Models
    print_neon_separator()
    print("Running Traditional NLP Models...")
    trad_classifier = TraditionalClassifier()
    trad_results = trad_classifier.train_and_evaluate(df)
    all_results.update(trad_results)
    
    # 3. NLU Models
    print_neon_separator()
    print("Running NLU Models (DistilBERT)...")
    nlu_classifier = NLUClassifier()
    nlu_results = nlu_classifier.train_and_evaluate(df)
    all_results.update(nlu_results)
    
    # 4. LLM Models
    print_neon_separator()
    print("Running LLM Models (Gemini)...")
    llm_classifier = LLMClassifier()
    llm_results = llm_classifier.evaluate(df, subset_size=5) # Small subset for demo speed
    all_results.update(llm_results)
    
    # 5. Comparison & Report
    print_header("Benchmark Results")
    
    # Table
    print(f"{'Model':<25} | {'Accuracy':<10} | {'F1 Score':<10}")
    print("-" * 50)
    best_model = None
    best_f1 = -1
    
    for model, metrics in all_results.items():
        print(f"{model:<25} | {metrics['accuracy']:.4f}     | {metrics['f1']:.4f}")
        if metrics['f1'] > best_f1:
            best_f1 = metrics['f1']
            best_model = model
            
    print("-" * 50)
    
    # Analytical Report
    report = [
        f"The best performing model is {best_model} with an F1 score of {best_f1:.4f}.",
        "Traditional models (SVM/LR) provide a strong baseline with low compute cost.",
        "DistilBERT offers better contextual understanding but requires training time.",
        "Gemini (Zero-shot) shows promise for unlabeled data but has higher latency."
    ]
    print_card("Analytical Report", report)

if __name__ == "__main__":
    run_benchmark()
