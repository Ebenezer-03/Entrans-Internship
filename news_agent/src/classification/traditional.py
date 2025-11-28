import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

class TraditionalClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000)
        self.models = {
            "SVM": SVC(kernel='linear'),
            "Logistic Regression": LogisticRegression(max_iter=1000),
            "Naive Bayes": MultinomialNB()
        }
        
    def train_and_evaluate(self, df, text_col='clean_text', label_col='label'):
        X = df[text_col]
        y = df[label_col]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Vectorize
        X_train_vec = self.vectorizer.fit_transform(X_train)
        X_test_vec = self.vectorizer.transform(X_test)
        
        results = {}
        
        for name, model in self.models.items():
            print(f"Training {name}...")
            model.fit(X_train_vec, y_train)
            preds = model.predict(X_test_vec)
            
            metrics = {
                "accuracy": accuracy_score(y_test, preds),
                "precision": precision_score(y_test, preds, average='weighted', zero_division=0),
                "recall": recall_score(y_test, preds, average='weighted', zero_division=0),
                "f1": f1_score(y_test, preds, average='weighted', zero_division=0),
                "confusion_matrix": confusion_matrix(y_test, preds).tolist()
            }
            results[name] = metrics
            
        return results
