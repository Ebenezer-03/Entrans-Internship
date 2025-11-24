"""
Day 2: Sentiment Classification with spaCy and sklearn

Demonstrates:
- spaCy TextCategorizer for sentiment analysis
- sklearn LogisticRegression baseline
- TF-IDF + SVM classifier
- Model comparison and evaluation

Expected Runtime: ~2 minutes (CPU)
Input: IMDB sentiment dataset
Output: Trained models, evaluation metrics, confusion matrix

Author: NLP/NLU 3-Day Project
"""

import logging
from pathlib import Path
from typing import Tuple, List
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
from spacy.training import Example

import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.metrics import (
    calculate_classification_metrics,
    print_classification_report,
    plot_confusion_matrix
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_sentiment_data() -> Tuple[List[str], List[int]]:
    """
    Load sentiment dataset.
    
    Returns:
        Tuple of (texts, labels)
    """
    data_path = Path(__file__).parent.parent / "data" / "samples" / "sentiment_small.csv"
    
    if data_path.exists():
        df = pd.read_csv(data_path)
        logger.info(f"Loaded {len(df)} samples from {data_path}")
        return df['text'].tolist(), df['label'].tolist()
    else:
        logger.warning(f"Dataset not found: {data_path}")
        logger.info("Creating sample data...")
        
        texts = [
            "This movie was fantastic! I loved it.",
            "Terrible film, complete waste of time.",
            "Great acting and beautiful visuals.",
            "Boring and predictable.",
        ] * 50
        labels = [1, 0, 1, 0] * 50
        
        return texts, labels


def train_sklearn_baseline(
    X_train: List[str],
    y_train: List[int],
    X_test: List[str],
    y_test: List[int]
) -> dict:
    """
    Train sklearn baseline with TF-IDF + Logistic Regression.
    
    Args:
        X_train: Training texts
        y_train: Training labels
        X_test: Test texts
        y_test: Test labels
        
    Returns:
        Dictionary with model, vectorizer, and metrics
    """
    logger.info("\n" + "=" * 80)
    logger.info("SKLEARN BASELINE: TF-IDF + LOGISTIC REGRESSION")
    logger.info("=" * 80)
    
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.95
    )
    
    # Transform data
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    logger.info(f"\nTF-IDF matrix shape: {X_train_tfidf.shape}")
    logger.info(f"Vocabulary size: {len(vectorizer.get_feature_names_out())}")
    
    # Train classifier
    logger.info("\nTraining Logistic Regression...")
    clf = LogisticRegression(max_iter=1000, random_state=42)
    clf.fit(X_train_tfidf, y_train)
    
    # Evaluate
    y_pred = clf.predict(X_test_tfidf)
    metrics = calculate_classification_metrics(y_test, y_pred)
    
    logger.info("\nTest Set Performance:")
    logger.info(f"  Accuracy:  {metrics['accuracy']:.4f}")
    logger.info(f"  Precision: {metrics['precision']:.4f}")
    logger.info(f"  Recall:    {metrics['recall']:.4f}")
    logger.info(f"  F1 Score:  {metrics['f1']:.4f}")
    
    return {
        'model': clf,
        'vectorizer': vectorizer,
        'metrics': metrics,
        'predictions': y_pred
    }


def train_spacy_textcat(
    X_train: List[str],
    y_train: List[int],
    X_test: List[str],
    y_test: List[int],
    n_iter: int = 10
) -> dict:
    """
    Train spaCy TextCategorizer.
    
    Args:
        X_train: Training texts
        y_train: Training labels
        X_test: Test texts
        y_test: Test labels
        n_iter: Number of training iterations
        
    Returns:
        Dictionary with model and metrics
    """
    logger.info("\n" + "=" * 80)
    logger.info("SPACY TEXT CATEGORIZER")
    logger.info("=" * 80)
    
    # Create blank spaCy model
    nlp = spacy.blank("en")
    
    # Add text categorizer
    textcat = nlp.add_pipe("textcat", last=True)
    textcat.add_label("POSITIVE")
    textcat.add_label("NEGATIVE")
    
    logger.info(f"\nTraining for {n_iter} iterations...")
    
    # Prepare training data
    train_data = []
    for text, label in zip(X_train, y_train):
        cats = {"POSITIVE": label == 1, "NEGATIVE": label == 0}
        train_data.append((text, {"cats": cats}))
    
    # Training loop
    nlp.begin_training()
    for i in range(n_iter):
        losses = {}
        
        # Create examples
        examples = []
        for text, annotations in train_data:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            examples.append(example)
        
        # Update model
        nlp.update(examples, drop=0.2, losses=losses)
        
        if (i + 1) % 5 == 0:
            logger.info(f"  Iteration {i+1}/{n_iter}, Loss: {losses['textcat']:.4f}")
    
    # Evaluate
    logger.info("\nEvaluating on test set...")
    y_pred = []
    for text in X_test:
        doc = nlp(text)
        pred = 1 if doc.cats["POSITIVE"] > doc.cats["NEGATIVE"] else 0
        y_pred.append(pred)
    
    metrics = calculate_classification_metrics(y_test, y_pred)
    
    logger.info("\nTest Set Performance:")
    logger.info(f"  Accuracy:  {metrics['accuracy']:.4f}")
    logger.info(f"  Precision: {metrics['precision']:.4f}")
    logger.info(f"  Recall:    {metrics['recall']:.4f}")
    logger.info(f"  F1 Score:  {metrics['f1']:.4f}")
    
    return {
        'model': nlp,
        'metrics': metrics,
        'predictions': y_pred
    }


def compare_models(sklearn_results: dict, spacy_results: dict) -> None:
    """
    Compare model performance.
    
    Args:
        sklearn_results: sklearn model results
        spacy_results: spaCy model results
    """
    logger.info("\n" + "=" * 80)
    logger.info("MODEL COMPARISON")
    logger.info("=" * 80)
    
    comparison = pd.DataFrame({
        'Model': ['sklearn (TF-IDF + LogReg)', 'spaCy (TextCat)'],
        'Accuracy': [
            sklearn_results['metrics']['accuracy'],
            spacy_results['metrics']['accuracy']
        ],
        'Precision': [
            sklearn_results['metrics']['precision'],
            spacy_results['metrics']['precision']
        ],
        'Recall': [
            sklearn_results['metrics']['recall'],
            spacy_results['metrics']['recall']
        ],
        'F1': [
            sklearn_results['metrics']['f1'],
            spacy_results['metrics']['f1']
        ]
    })
    
    logger.info("\n" + comparison.to_string(index=False))


def main():
    """Main demonstration function."""
    logger.info("=" * 80)
    logger.info("DAY 2: SENTIMENT CLASSIFICATION")
    logger.info("=" * 80)
    
    # Load data
    texts, labels = load_sentiment_data()
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )
    
    logger.info(f"\nDataset split:")
    logger.info(f"  Training samples: {len(X_train)}")
    logger.info(f"  Test samples: {len(X_test)}")
    
    # Train sklearn baseline
    sklearn_results = train_sklearn_baseline(X_train, y_train, X_test, y_test)
    
    # Train spaCy model (fewer iterations for demo)
    spacy_results = train_spacy_textcat(X_train, y_train, X_test, y_test, n_iter=10)
    
    # Compare models
    compare_models(sklearn_results, spacy_results)
    
    # Print detailed classification report
    print_classification_report(
        y_test,
        sklearn_results['predictions'],
        target_names=['Negative', 'Positive']
    )
    
    # Plot confusion matrix
    output_dir = Path(__file__).parent.parent / "examples" / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    plot_confusion_matrix(
        y_test,
        sklearn_results['predictions'],
        labels=['Negative', 'Positive'],
        save_path=str(output_dir / "confusion_matrix_sentiment.png")
    )
    
    logger.info("\n" + "=" * 80)
    logger.info("DEMO COMPLETE")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
