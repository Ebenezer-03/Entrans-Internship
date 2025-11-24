"""
Day 2: Bag of Words and TF-IDF

Demonstrates:
- Bag of Words from scratch
- sklearn CountVectorizer
- TF-IDF manual calculation
- sklearn TfidfVectorizer
- Feature importance visualization

Expected Runtime: ~1 minute (CPU)
Input: Text corpus or CSV file
Output: BOW/TF-IDF matrices, feature importance

Author: NLP/NLU 3-Day Project
"""

import argparse
import logging
from pathlib import Path
from typing import List, Dict, Tuple
from collections import Counter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def bag_of_words_from_scratch(documents: List[str]) -> Tuple[np.ndarray, List[str]]:
    """
    Create Bag of Words representation from scratch.
    
    Args:
        documents: List of text documents
        
    Returns:
        Tuple of (BOW matrix, vocabulary list)
    """
    logger.info("\n" + "=" * 80)
    logger.info("BAG OF WORDS FROM SCRATCH")
    logger.info("=" * 80)
    
    # Build vocabulary
    vocabulary = set()
    for doc in documents:
        words = doc.lower().split()
        vocabulary.update(words)
    
    vocabulary = sorted(list(vocabulary))
    word_to_idx = {word: idx for idx, word in enumerate(vocabulary)}
    
    logger.info(f"\nVocabulary size: {len(vocabulary)}")
    logger.info(f"First 10 words: {vocabulary[:10]}")
    
    # Create BOW matrix
    bow_matrix = np.zeros((len(documents), len(vocabulary)), dtype=int)
    
    for doc_idx, doc in enumerate(documents):
        words = doc.lower().split()
        word_counts = Counter(words)
        
        for word, count in word_counts.items():
            if word in word_to_idx:
                bow_matrix[doc_idx, word_to_idx[word]] = count
    
    logger.info(f"\nBOW matrix shape: {bow_matrix.shape}")
    logger.info(f"Sparsity: {(bow_matrix == 0).sum() / bow_matrix.size:.2%}")
    
    return bow_matrix, vocabulary


def demonstrate_count_vectorizer(documents: List[str]) -> Tuple[np.ndarray, List[str]]:
    """
    Demonstrate sklearn CountVectorizer.
    
    Args:
        documents: List of text documents
        
    Returns:
        Tuple of (BOW matrix, feature names)
    """
    logger.info("\n" + "=" * 80)
    logger.info("SKLEARN COUNT VECTORIZER")
    logger.info("=" * 80)
    
    # Create vectorizer
    vectorizer = CountVectorizer(
        max_features=100,
        ngram_range=(1, 2),
        min_df=1,
        max_df=0.95
    )
    
    # Fit and transform
    bow_matrix = vectorizer.fit_transform(documents)
    feature_names = vectorizer.get_feature_names_out()
    
    logger.info(f"\nVectorizer parameters:")
    logger.info(f"  - max_features: 100")
    logger.info(f"  - ngram_range: (1, 2)")
    logger.info(f"  - min_df: 1")
    logger.info(f"  - max_df: 0.95")
    
    logger.info(f"\nBOW matrix shape: {bow_matrix.shape}")
    logger.info(f"Vocabulary size: {len(feature_names)}")
    logger.info(f"Sparsity: {(bow_matrix.toarray() == 0).sum() / bow_matrix.toarray().size:.2%}")
    
    # Show top features
    logger.info(f"\nTop 20 features: {list(feature_names[:20])}")
    
    return bow_matrix.toarray(), list(feature_names)


def tfidf_from_scratch(documents: List[str]) -> Tuple[np.ndarray, List[str]]:
    """
    Calculate TF-IDF from scratch.
    
    Args:
        documents: List of text documents
        
    Returns:
        Tuple of (TF-IDF matrix, vocabulary)
    """
    logger.info("\n" + "=" * 80)
    logger.info("TF-IDF FROM SCRATCH")
    logger.info("=" * 80)
    
    # Get BOW first
    bow_matrix, vocabulary = bag_of_words_from_scratch(documents)
    
    # Calculate TF (term frequency)
    tf_matrix = bow_matrix / (bow_matrix.sum(axis=1, keepdims=True) + 1e-10)
    
    # Calculate IDF (inverse document frequency)
    doc_count = len(documents)
    df = (bow_matrix > 0).sum(axis=0)  # Document frequency
    idf = np.log((doc_count + 1) / (df + 1)) + 1
    
    # Calculate TF-IDF
    tfidf_matrix = tf_matrix * idf
    
    logger.info(f"\nTF-IDF matrix shape: {tfidf_matrix.shape}")
    logger.info(f"TF-IDF range: [{tfidf_matrix.min():.4f}, {tfidf_matrix.max():.4f}]")
    
    return tfidf_matrix, vocabulary


def demonstrate_tfidf_vectorizer(documents: List[str]) -> Tuple[np.ndarray, List[str]]:
    """
    Demonstrate sklearn TfidfVectorizer.
    
    Args:
        documents: List of text documents
        
    Returns:
        Tuple of (TF-IDF matrix, feature names)
    """
    logger.info("\n" + "=" * 80)
    logger.info("SKLEARN TFIDF VECTORIZER")
    logger.info("=" * 80)
    
    # Create vectorizer
    vectorizer = TfidfVectorizer(
        max_features=100,
        ngram_range=(1, 2),
        min_df=1,
        max_df=0.95,
        sublinear_tf=True
    )
    
    # Fit and transform
    tfidf_matrix = vectorizer.fit_transform(documents)
    feature_names = vectorizer.get_feature_names_out()
    
    logger.info(f"\nVectorizer parameters:")
    logger.info(f"  - max_features: 100")
    logger.info(f"  - ngram_range: (1, 2)")
    logger.info(f"  - sublinear_tf: True")
    
    logger.info(f"\nTF-IDF matrix shape: {tfidf_matrix.shape}")
    logger.info(f"Vocabulary size: {len(feature_names)}")
    
    return tfidf_matrix.toarray(), list(feature_names)


def visualize_feature_importance(
    tfidf_matrix: np.ndarray,
    feature_names: List[str],
    top_n: int = 20,
    save_path: str = None
) -> None:
    """
    Visualize top TF-IDF features.
    
    Args:
        tfidf_matrix: TF-IDF matrix
        feature_names: Feature names
        top_n: Number of top features to show
        save_path: Optional path to save figure
    """
    logger.info("\n" + "=" * 80)
    logger.info("FEATURE IMPORTANCE VISUALIZATION")
    logger.info("=" * 80)
    
    # Calculate mean TF-IDF scores
    mean_tfidf = tfidf_matrix.mean(axis=0)
    
    # Get top features
    top_indices = np.argsort(mean_tfidf)[-top_n:][::-1]
    top_features = [feature_names[i] for i in top_indices]
    top_scores = [mean_tfidf[i] for i in top_indices]
    
    logger.info(f"\nTop {top_n} features by mean TF-IDF:")
    for feature, score in zip(top_features, top_scores):
        logger.info(f"  {feature:20s}: {score:.4f}")
    
    # Plot
    plt.figure(figsize=(10, 6))
    plt.barh(range(len(top_features)), top_scores, color='steelblue')
    plt.yticks(range(len(top_features)), top_features)
    plt.xlabel('Mean TF-IDF Score', fontsize=12)
    plt.title(f'Top {top_n} Features by TF-IDF', fontsize=14, fontweight='bold')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"\nFigure saved to: {save_path}")
    
    plt.show()


def load_dataset(dataset_path: str) -> Tuple[List[str], List[int]]:
    """
    Load dataset from CSV file.
    
    Args:
        dataset_path: Path to CSV file
        
    Returns:
        Tuple of (texts, labels)
    """
    logger.info(f"\nLoading dataset from: {dataset_path}")
    
    df = pd.read_csv(dataset_path)
    texts = df['text'].tolist()
    labels = df['label'].tolist() if 'label' in df.columns else None
    
    logger.info(f"Loaded {len(texts)} samples")
    
    return texts, labels


def main():
    """Main demonstration function."""
    parser = argparse.ArgumentParser(description='BOW and TF-IDF demonstration')
    parser.add_argument(
        '--dataset',
        type=str,
        default=None,
        help='Path to CSV dataset (optional)'
    )
    args = parser.parse_args()
    
    logger.info("=" * 80)
    logger.info("DAY 2: BAG OF WORDS AND TF-IDF")
    logger.info("=" * 80)
    
    # Sample documents
    if args.dataset and Path(args.dataset).exists():
        documents, _ = load_dataset(args.dataset)
        documents = documents[:100]  # Use first 100 for demo
    else:
        documents = [
            "The cat sat on the mat.",
            "The dog played in the park.",
            "Cats and dogs are popular pets.",
            "The quick brown fox jumps over the lazy dog.",
            "Machine learning is a subset of artificial intelligence.",
            "Natural language processing enables computers to understand text.",
            "Deep learning uses neural networks with multiple layers.",
        ]
    
    logger.info(f"\nUsing {len(documents)} documents for demonstration")
    
    # BOW demonstrations
    bow_scratch, vocab_scratch = bag_of_words_from_scratch(documents)
    bow_sklearn, features_sklearn = demonstrate_count_vectorizer(documents)
    
    # TF-IDF demonstrations
    tfidf_scratch, _ = tfidf_from_scratch(documents)
    tfidf_sklearn, tfidf_features = demonstrate_tfidf_vectorizer(documents)
    
    # Visualization
    output_dir = Path(__file__).parent.parent / "examples" / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    visualize_feature_importance(
        tfidf_sklearn,
        tfidf_features,
        top_n=20,
        save_path=str(output_dir / "tfidf_features.png")
    )
    
    logger.info("\n" + "=" * 80)
    logger.info("DEMO COMPLETE")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
