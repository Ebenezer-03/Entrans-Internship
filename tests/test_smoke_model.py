"""
Smoke test: Train a simple classifier on minimal data.

This test ensures that the basic ML pipeline works end-to-end.
Should complete in < 10 seconds.
"""

import sys
from pathlib import Path
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

sys.path.append(str(Path(__file__).parent.parent))
from utils.metrics import calculate_classification_metrics


def test_smoke_classifier():
    """Smoke test for basic classifier pipeline."""
    print("\n" + "=" * 80)
    print("SMOKE TEST: Training Minimal Classifier")
    print("=" * 80)
    
    # Create minimal dataset
    texts = [
        "This is a positive example",
        "Great and wonderful",
        "Excellent work",
        "This is negative",
        "Bad and terrible",
        "Awful experience",
    ] * 10  # 60 samples
    
    labels = [1, 1, 1, 0, 0, 0] * 10
    
    print(f"\nDataset: {len(texts)} samples")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42
    )
    
    print(f"Train: {len(X_train)}, Test: {len(X_test)}")
    
    # Vectorize
    vectorizer = TfidfVectorizer(max_features=50)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    print(f"Feature matrix shape: {X_train_vec.shape}")
    
    # Train classifier
    clf = LogisticRegression(max_iter=100, random_state=42)
    clf.fit(X_train_vec, y_train)
    
    print("Model trained successfully")
    
    # Evaluate
    y_pred = clf.predict(X_test_vec)
    metrics = calculate_classification_metrics(y_test, y_pred)
    
    print(f"\nTest Accuracy: {metrics['accuracy']:.4f}")
    print(f"F1 Score: {metrics['f1']:.4f}")
    
    # Assert basic sanity checks
    assert metrics['accuracy'] > 0.5, "Accuracy too low"
    assert len(y_pred) == len(y_test), "Prediction length mismatch"
    
    print("\n" + "=" * 80)
    print("SMOKE TEST PASSED ✓")
    print("=" * 80)
    
    return True


if __name__ == "__main__":
    try:
        test_smoke_classifier()
        sys.exit(0)
    except Exception as e:
        print(f"\nSMOKE TEST FAILED: {e}")
        sys.exit(1)
