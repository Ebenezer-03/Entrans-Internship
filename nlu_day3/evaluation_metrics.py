"""
Day 3: Evaluation Metrics for NLU Tasks

Demonstrates:
- ROUGE score calculation and interpretation
- BLEU score calculation and interpretation
- Usage examples for summarization and translation

Author: NLP/NLU 3-Day Project
"""

import logging
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from utils.metrics import (
    calculate_rouge_scores,
    calculate_bleu_score,
    print_rouge_scores,
    print_bleu_score
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def demonstrate_rouge() -> None:
    """Demonstrate ROUGE score calculation."""
    logger.info("\n" + "=" * 80)
    logger.info("ROUGE SCORE DEMONSTRATION")
    logger.info("=" * 80)
    
    # Example summaries
    predictions = [
        "The cat sat on the mat and looked around.",
        "Machine learning is a subset of artificial intelligence."
    ]
    
    references = [
        "The cat was sitting on the mat.",
        "Machine learning is part of AI and uses algorithms."
    ]
    
    logger.info("\nExample 1:")
    logger.info(f"  Prediction: {predictions[0]}")
    logger.info(f"  Reference:  {references[0]}")
    
    logger.info("\nExample 2:")
    logger.info(f"  Prediction: {predictions[1]}")
    logger.info(f"  Reference:  {references[1]}")
    
    # Calculate ROUGE
    scores = calculate_rouge_scores(predictions, references)
    print_rouge_scores(scores)
    
    # Interpretation
    logger.info("\nInterpretation:")
    logger.info("  - ROUGE-1: Unigram overlap (individual word matches)")
    logger.info("  - ROUGE-2: Bigram overlap (two consecutive word matches)")
    logger.info("  - ROUGE-L: Longest common subsequence")
    logger.info("  - Higher scores = better summary quality")
    logger.info("  - Typical good scores: ROUGE-1 > 0.4, ROUGE-2 > 0.2")


def demonstrate_bleu() -> None:
    """Demonstrate BLEU score calculation."""
    logger.info("\n" + "=" * 80)
    logger.info("BLEU SCORE DEMONSTRATION")
    logger.info("=" * 80)
    
    # Example translations
    predictions = [
        "The cat is on the mat",
        "I am learning natural language processing"
    ]
    
    references = [
        ["The cat sits on the mat"],
        ["I am studying natural language processing"]
    ]
    
    logger.info("\nExample 1:")
    logger.info(f"  Prediction: {predictions[0]}")
    logger.info(f"  Reference:  {references[0][0]}")
    
    logger.info("\nExample 2:")
    logger.info(f"  Prediction: {predictions[1]}")
    logger.info(f"  Reference:  {references[1][0]}")
    
    # Calculate BLEU
    score = calculate_bleu_score(predictions, references)
    print_bleu_score(score)
    
    # Interpretation
    logger.info("\nInterpretation:")
    logger.info("  - BLEU: Bilingual Evaluation Understudy")
    logger.info("  - Measures n-gram precision with brevity penalty")
    logger.info("  - Score range: 0-100 (higher is better)")
    logger.info("  - Typical scores:")
    logger.info("    * > 40: High quality")
    logger.info("    * 30-40: Understandable")
    logger.info("    * 20-30: Comprehensible")
    logger.info("    * < 20: Poor quality")


def rouge_vs_bleu_comparison() -> None:
    """Compare ROUGE and BLEU metrics."""
    logger.info("\n" + "=" * 80)
    logger.info("ROUGE VS BLEU COMPARISON")
    logger.info("=" * 80)
    
    comparison = """
    ROUGE (Recall-Oriented Understudy for Gisting Evaluation):
    - Primary use: Summarization evaluation
    - Focus: Recall (how much of reference is captured)
    - Variants: ROUGE-N (n-grams), ROUGE-L (longest common subsequence)
    - Range: 0-1 (F1, precision, recall)
    - Advantage: Captures content overlap well
    
    BLEU (Bilingual Evaluation Understudy):
    - Primary use: Machine translation evaluation
    - Focus: Precision (how much of prediction is correct)
    - Variants: BLEU-1, BLEU-2, BLEU-3, BLEU-4 (n-gram precision)
    - Range: 0-100
    - Advantage: Penalizes overly short outputs (brevity penalty)
    
    When to use:
    - ROUGE: Summarization, content extraction
    - BLEU: Translation, text generation
    - Both: Can complement each other for comprehensive evaluation
    """
    
    logger.info(comparison)


def main():
    """Main demonstration function."""
    logger.info("=" * 80)
    logger.info("DAY 3: EVALUATION METRICS (ROUGE & BLEU)")
    logger.info("=" * 80)
    
    # Demonstrate ROUGE
    demonstrate_rouge()
    
    # Demonstrate BLEU
    demonstrate_bleu()
    
    # Compare metrics
    rouge_vs_bleu_comparison()
    
    logger.info("\n" + "=" * 80)
    logger.info("DEMO COMPLETE")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
