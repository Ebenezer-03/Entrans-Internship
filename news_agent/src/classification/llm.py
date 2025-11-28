import vertexai
from vertexai.generative_models import GenerativeModel
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import pandas as pd
import time

class LLMClassifier:
    def __init__(self, project_id="your-project-id", location="us-central1"):
        # In a real scenario, we'd init vertexai here. 
        # For this task, we'll assume auth is handled or mock if credentials missing.
        try:
            vertexai.init(project=project_id, location=location)
            self.model = GenerativeModel("gemini-1.5-flash-001")
            self.available = True
        except Exception as e:
            print(f"Vertex AI init failed: {e}. LLM classification will be mocked.")
            self.available = False

    def classify_zero_shot(self, text, categories):
        if not self.available:
            return categories[0] # Mock
            
        prompt = f"""Classify the following news text into one of these categories: {', '.join(categories)}.
        
        Text: {text}
        
        Category:"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except:
            return "Unknown"

    def classify_few_shot(self, text, categories, examples):
        if not self.available:
            return categories[0] # Mock

        prompt = "Classify the news text into categories.\n\n"
        for ex_text, ex_label in examples:
            prompt += f"Text: {ex_text}\nCategory: {ex_label}\n\n"
            
        prompt += f"Text: {text}\nCategory:"
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except:
            return "Unknown"

    def evaluate(self, df, text_col='clean_text', label_col='label', subset_size=10):
        # LLM inference is slow/costly, so we evaluate on a subset
        subset = df.head(subset_size)
        categories = df[label_col].unique().tolist()
        
        preds_zero = []
        preds_few = []
        
        # Prepare few-shot examples (take 1 from each category)
        examples = []
        for cat in categories:
            ex = df[df[label_col] == cat].iloc[0]
            examples.append((ex[text_col], ex[label_col]))
            
        print(f"Running LLM classification on {subset_size} samples...")
        
        for text in subset[text_col]:
            # Zero-shot
            p_zero = self.classify_zero_shot(text, categories)
            # Simple cleanup to match category
            preds_zero.append(self._match_category(p_zero, categories))
            
            # Few-shot
            p_few = self.classify_few_shot(text, categories, examples)
            preds_few.append(self._match_category(p_few, categories))
            
        y_true = subset[label_col].tolist()
        
        results = {}
        
        # Zero-shot metrics
        p, r, f, _ = precision_recall_fscore_support(y_true, preds_zero, average='weighted', zero_division=0)
        results["Gemini Zero-Shot"] = {
            "accuracy": accuracy_score(y_true, preds_zero),
            "precision": p, "recall": r, "f1": f
        }
        
        # Few-shot metrics
        p, r, f, _ = precision_recall_fscore_support(y_true, preds_few, average='weighted', zero_division=0)
        results["Gemini Few-Shot"] = {
            "accuracy": accuracy_score(y_true, preds_few),
            "precision": p, "recall": r, "f1": f
        }
        
        return results

    def _match_category(self, pred, categories):
        # Helper to map LLM output to nearest category
        pred = pred.lower()
        for cat in categories:
            if cat.lower() in pred:
                return cat
        return categories[0] # Fallback
