"""
Evaluation Metrics Utilities

Provides reusable metric calculation functions for classification,
regression, and text generation tasks (ROUGE, BLEU).

Author: NLP/NLU 3-Day Project
"""

from typing import List, Dict, Any, Optional, Union
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix,
    classification_report
)
import matplotlib.pyplot as plt
import seaborn as sns
from rouge_score import rouge_scorer
from sacrebleu.metrics import BLEU


def calculate_classification_metrics(
    y_true: List[Any],
    y_pred: List[Any],
    labels: Optional[List[str]] = None
) -> Dict[str, float]:
    """
    Calculate comprehensive classification metrics.
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        labels: Label names for reporting
        
    Returns:
        Dictionary with accuracy, precision, recall, F1
    """
    accuracy = accuracy_score(y_true, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average='weighted', zero_division=0
    )
    
    metrics = {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1
    }
    
    return metrics


def print_classification_report(
    y_true: List[Any],
    y_pred: List[Any],
    target_names: Optional[List[str]] = None
) -> None:
    """
    Print detailed classification report.
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        target_names: Class names
    """
    print("\nClassification Report:")
    print("=" * 60)
    print(classification_report(y_true, y_pred, target_names=target_names))
    print("=" * 60)


def plot_confusion_matrix(
    y_true: List[Any],
    y_pred: List[Any],
    labels: Optional[List[str]] = None,
    save_path: Optional[str] = None,
    figsize: tuple = (8, 6)
) -> None:
    """
    Plot confusion matrix heatmap.
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        labels: Class names
        save_path: Path to save figure (optional)
        figsize: Figure size
    """
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=figsize)
    sns.heatmap(
        cm,
        annot=True,
        fmt='d',
        cmap='Blues',
        xticklabels=labels,
        yticklabels=labels,
        cbar_kws={'label': 'Count'}
    )
    plt.title('Confusion Matrix', fontsize=14, fontweight='bold')
    plt.ylabel('True Label', fontsize=12)
    plt.xlabel('Predicted Label', fontsize=12)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Confusion matrix saved to {save_path}")
    
    plt.show()


def calculate_rouge_scores(
    predictions: List[str],
    references: List[str],
    rouge_types: List[str] = ["rouge1", "rouge2", "rougeL"]
) -> Dict[str, Dict[str, float]]:
    """
    Calculate ROUGE scores for text generation.
    
    Args:
        predictions: Generated texts
        references: Reference texts
        rouge_types: ROUGE variants to compute
        
    Returns:
        Dictionary with ROUGE scores (precision, recall, F1)
        
    Example:
        >>> preds = ["the cat sat on the mat"]
        >>> refs = ["the cat is on the mat"]
        >>> scores = calculate_rouge_scores(preds, refs)
        >>> print(scores["rouge1"]["fmeasure"])
    """
    scorer = rouge_scorer.RougeScorer(rouge_types, use_stemmer=True)
    
    all_scores = {rouge_type: [] for rouge_type in rouge_types}
    
    for pred, ref in zip(predictions, references):
        scores = scorer.score(ref, pred)
        for rouge_type in rouge_types:
            all_scores[rouge_type].append(scores[rouge_type])
    
    # Average scores
    avg_scores = {}
    for rouge_type in rouge_types:
        avg_scores[rouge_type] = {
            "precision": np.mean([s.precision for s in all_scores[rouge_type]]),
            "recall": np.mean([s.recall for s in all_scores[rouge_type]]),
            "fmeasure": np.mean([s.fmeasure for s in all_scores[rouge_type]])
        }
    
    return avg_scores


def calculate_bleu_score(
    predictions: List[str],
    references: List[List[str]],
    smooth: bool = True
) -> Dict[str, float]:
    """
    Calculate BLEU score for text generation.
    
    Args:
        predictions: Generated texts
        references: List of reference texts (can be multiple per prediction)
        smooth: Apply smoothing for short texts
        
    Returns:
        Dictionary with BLEU score and components
        
    Example:
        >>> preds = ["the cat sat on the mat"]
        >>> refs = [["the cat is on the mat"]]
        >>> score = calculate_bleu_score(preds, refs)
        >>> print(score["score"])
    """
    bleu = BLEU(smooth_method='exp' if smooth else 'none')
    
    # sacrebleu expects references as list of lists
    if isinstance(references[0], str):
        references = [[ref] for ref in references]
    
    # Transpose references for sacrebleu format
    refs_transposed = list(zip(*references))
    
    result = bleu.corpus_score(predictions, refs_transposed)
    
    return {
        "score": result.score,
        "precisions": result.precisions,
        "bp": result.bp,
        "sys_len": result.sys_len,
        "ref_len": result.ref_len
    }


def print_rouge_scores(scores: Dict[str, Dict[str, float]]) -> None:
    """
    Pretty print ROUGE scores.
    
    Args:
        scores: ROUGE scores dictionary from calculate_rouge_scores
    """
    print("\nROUGE Scores:")
    print("=" * 60)
    for rouge_type, metrics in scores.items():
        print(f"\n{rouge_type.upper()}:")
        print(f"  Precision: {metrics['precision']:.4f}")
        print(f"  Recall:    {metrics['recall']:.4f}")
        print(f"  F1:        {metrics['fmeasure']:.4f}")
    print("=" * 60)


def print_bleu_score(score_dict: Dict[str, float]) -> None:
    """
    Pretty print BLEU score.
    
    Args:
        score_dict: BLEU score dictionary from calculate_bleu_score
    """
    print("\nBLEU Score:")
    print("=" * 60)
    print(f"  Score: {score_dict['score']:.2f}")
    print(f"  Brevity Penalty: {score_dict['bp']:.4f}")
    print(f"  System Length: {score_dict['sys_len']}")
    print(f"  Reference Length: {score_dict['ref_len']}")
    print("=" * 60)


if __name__ == "__main__":
    # Example usage for classification metrics
    print("Classification Metrics Example:")
    y_true = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    y_pred = [0, 1, 2, 0, 2, 1, 0, 1, 1]
    labels = ["Class A", "Class B", "Class C"]
    
    metrics = calculate_classification_metrics(y_true, y_pred)
    print(f"\nAccuracy: {metrics['accuracy']:.4f}")
    print(f"F1 Score: {metrics['f1']:.4f}")
    
    print_classification_report(y_true, y_pred, target_names=labels)
    
    # Example usage for ROUGE
    print("\n\nROUGE Metrics Example:")
    predictions = ["the cat sat on the mat"]
    references = ["the cat is on the mat"]
    
    rouge_scores = calculate_rouge_scores(predictions, references)
    print_rouge_scores(rouge_scores)
    
    # Example usage for BLEU
    print("\n\nBLEU Metrics Example:")
    bleu_score = calculate_bleu_score(predictions, [references])
    print_bleu_score(bleu_score)
