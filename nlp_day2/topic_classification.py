"""
Day 2: Topic Classification

Demonstrates:
- Multi-class classification with TF-IDF + SVM
- AG News topic classification
- Model evaluation and confusion matrix
- Feature importance analysis

Expected Runtime: ~2 minutes (CPU)
Input: AG News dataset
Output: Trained classifier, evaluation metrics

Author: NLP/NLU 3-Day Project
"""

import logging
from pathlib import Path
from typing import Tuple, List
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer

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

# Topic labels
TOPIC_LABELS = {
    0: "World",
    1: "Sports",
    2: "Business",
    3: "Sci/Tech"
}


def load_topic_data() -> Tuple[List[str], List[int]]:
    """
    Load topic classification dataset.
    
    Returns:
        Tuple of (texts, labels)
    """
    data_path = Path(__file__).parent.parent / "data" / "samples" / "topics_small.csv"
    
    if data_path.exists():
        df = pd.read_csv(data_path)
        logger.info(f"Loaded {len(df)} samples from {data_path}")
        
        # Show class distribution
        logger.info("\nClass distribution:")
        for label, name in TOPIC_LABELS.items():
            count = (df['label'] == label).sum()
            logger.info(f"  {name}: {count}")
        
        return df['text'].tolist(), df['label'].tolist()
    else:
        logger.warning(f"Dataset not found: {data_path}")
        logger.info("Creating sample data...")
        
        texts = [
            "The stock market reached new highs today.",
            "Scientists discover new planet in distant galaxy.",
            "Local team wins championship game.",
            "New policy announced by government officials.",
        ] * 25
        labels = [2, 3, 1, 0] * 25
        
        return texts, labels


def train_topic_classifier(
    X_train: List[str],
    y_train: List[int],
    X_test: List[str],
    y_test: List[int]
) -> dict:
    """
    Train topic classifier with TF-IDF + SVM.
    
    Args:
        X_train: Training texts
        y_train: Training labels
        X_test: Test texts
        y_test: Test labels
        
    Returns:
        Dictionary with model, vectorizer, and metrics
    """
    logger.info("\n" + "=" * 80)
    logger.info("TOPIC CLASSIFICATION: TF-IDF + LINEAR SVM")
    logger.info("=" * 80)
    
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.95,
        sublinear_tf=True
    )
    
    # Transform data
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    logger.info(f"\nTF-IDF matrix shape: {X_train_tfidf.shape}")
    logger.info(f"Vocabulary size: {len(vectorizer.get_feature_names_out())}")
    
    # Train SVM classifier
    logger.info("\nTraining Linear SVM...")
    clf = LinearSVC(max_iter=1000, random_state=42)
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


def analyze_feature_importance(
    model: LinearSVC,
    vectorizer: TfidfVectorizer,
    top_n: int = 10
) -> None:
    """
    Analyze top features for each class.
    
    Args:
        model: Trained LinearSVC model
        vectorizer: Fitted TfidfVectorizer
        top_n: Number of top features per class
    """
    logger.info("\n" + "=" * 80)
    logger.info("FEATURE IMPORTANCE ANALYSIS")
    logger.info("=" * 80)
    
    feature_names = vectorizer.get_feature_names_out()
    
    for class_idx, class_name in TOPIC_LABELS.items():
        logger.info(f"\nTop {top_n} features for '{class_name}':")
        
        # Get coefficients for this class
        coef = model.coef_[class_idx]
        top_indices = np.argsort(coef)[-top_n:][::-1]
        
        for i, idx in enumerate(top_indices, 1):
            logger.info(f"  {i:2d}. {feature_names[idx]:20s} (coef: {coef[idx]:.4f})")


def predict_examples(
    model: LinearSVC,
    vectorizer: TfidfVectorizer,
    examples: List[str]
) -> None:
    """
    Predict topics for example texts.
    
    Args:
        model: Trained model
        vectorizer: Fitted vectorizer
        examples: Example texts
    """
    logger.info("\n" + "=" * 80)
    logger.info("PREDICTION EXAMPLES")
    logger.info("=" * 80)
    
    X_examples = vectorizer.transform(examples)
    predictions = model.predict(X_examples)
    
    for text, pred in zip(examples, predictions):
        logger.info(f"\nText: {text}")
        logger.info(f"Predicted Topic: {TOPIC_LABELS[pred]}")


def main():
    """Main demonstration function."""
    logger.info("=" * 80)
    logger.info("DAY 2: TOPIC CLASSIFICATION")
    logger.info("=" * 80)
    
    # Load data
    texts, labels = load_topic_data()
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )
    
    logger.info(f"\nDataset split:")
    logger.info(f"  Training samples: {len(X_train)}")
    logger.info(f"  Test samples: {len(X_test)}")
    
    # Train classifier
    results = train_topic_classifier(X_train, y_train, X_test, y_test)
    
    # Print detailed classification report
    topic_names = [TOPIC_LABELS[i] for i in range(len(TOPIC_LABELS))]
    print_classification_report(
        y_test,
        results['predictions'],
        target_names=topic_names
    )
    
    # Plot confusion matrix
    output_dir = Path(__file__).parent.parent / "examples" / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    plot_confusion_matrix(
        y_test,
        results['predictions'],
        labels=topic_names,
        save_path=str(output_dir / "confusion_matrix_topics.png")
    )
    
    # Analyze feature importance
    analyze_feature_importance(results['model'], results['vectorizer'], top_n=10)
    
    # Predict on new examples
    examples = [
        "The Federal Reserve announced new interest rate policies.",
        "NASA launches new Mars rover mission.",
        "Championship final draws record crowd.",
        "United Nations votes on climate resolution."
    ]
    predict_examples(results['model'], results['vectorizer'], examples)
    
    logger.info("\n" + "=" * 80)
    logger.info("DEMO COMPLETE")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
