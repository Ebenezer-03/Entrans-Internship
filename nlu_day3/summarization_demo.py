"""
Day 3: Text Summarization with Transformers

Demonstrates:
- Abstractive summarization using transformers pipeline
- ROUGE score evaluation
- BLEU score calculation
- Comparison of different summarization parameters

Expected Runtime: ~30 seconds (CPU)
Input: Article text file
Output: Generated summaries, ROUGE/BLEU scores

Author: NLP/NLU 3-Day Project
Usage:
    python summarization_demo.py --text_file data/samples/article.txt
"""

import argparse
import logging
from pathlib import Path
from typing import List, Dict
from transformers import pipeline

import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.metrics import calculate_rouge_scores, calculate_bleu_score, print_rouge_scores, print_bleu_score

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_article(file_path: str) -> str:
    """
    Load article from text file.
    
    Args:
        file_path: Path to text file
        
    Returns:
        Article text
    """
    logger.info(f"\nLoading article from: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read().strip()
    
    logger.info(f"Article length: {len(text)} characters, {len(text.split())} words")
    
    return text


def create_summarizer(model_name: str = "sshleifer/distilbart-cnn-6-6"):
    """
    Create summarization pipeline.
    
    Args:
        model_name: HuggingFace model name
        
    Returns:
        Summarization pipeline
    """
    logger.info(f"\nLoading summarization model: {model_name}")
    
    summarizer = pipeline(
        "summarization",
        model=model_name,
        device=-1  # CPU
    )
    
    logger.info("Model loaded successfully")
    
    return summarizer


def generate_summary(
    summarizer,
    text: str,
    max_length: int = 130,
    min_length: int = 30,
    do_sample: bool = False
) -> str:
    """
    Generate summary for text.
    
    Args:
        summarizer: Summarization pipeline
        text: Input text
        max_length: Maximum summary length
        min_length: Minimum summary length
        do_sample: Whether to use sampling
        
    Returns:
        Generated summary
    """
    logger.info("\n" + "=" * 80)
    logger.info("GENERATING SUMMARY")
    logger.info("=" * 80)
    
    logger.info(f"\nParameters:")
    logger.info(f"  max_length: {max_length}")
    logger.info(f"  min_length: {min_length}")
    logger.info(f"  do_sample: {do_sample}")
    
    # Generate summary
    result = summarizer(
        text,
        max_length=max_length,
        min_length=min_length,
        do_sample=do_sample,
        truncation=True
    )
    
    summary = result[0]['summary_text']
    
    logger.info(f"\nGenerated summary ({len(summary.split())} words):")
    logger.info(f"  {summary}")
    
    return summary


def demonstrate_different_lengths(summarizer, text: str) -> List[str]:
    """
    Generate summaries with different lengths.
    
    Args:
        summarizer: Summarization pipeline
        text: Input text
        
    Returns:
        List of summaries
    """
    logger.info("\n" + "=" * 80)
    logger.info("SUMMARIES WITH DIFFERENT LENGTHS")
    logger.info("=" * 80)
    
    configs = [
        {"max_length": 50, "min_length": 20, "name": "Short"},
        {"max_length": 100, "min_length": 40, "name": "Medium"},
        {"max_length": 150, "min_length": 60, "name": "Long"},
    ]
    
    summaries = []
    
    for config in configs:
        logger.info(f"\n{config['name']} Summary:")
        summary = generate_summary(
            summarizer,
            text,
            max_length=config['max_length'],
            min_length=config['min_length']
        )
        summaries.append(summary)
    
    return summaries


def evaluate_summary(
    generated_summary: str,
    reference_summary: str
) -> Dict:
    """
    Evaluate generated summary against reference.
    
    Args:
        generated_summary: Generated summary
        reference_summary: Reference summary
        
    Returns:
        Dictionary with ROUGE and BLEU scores
    """
    logger.info("\n" + "=" * 80)
    logger.info("SUMMARY EVALUATION")
    logger.info("=" * 80)
    
    logger.info(f"\nGenerated: {generated_summary}")
    logger.info(f"\nReference: {reference_summary}")
    
    # Calculate ROUGE scores
    rouge_scores = calculate_rouge_scores(
        [generated_summary],
        [reference_summary],
        rouge_types=["rouge1", "rouge2", "rougeL"]
    )
    
    print_rouge_scores(rouge_scores)
    
    # Calculate BLEU score
    bleu_score = calculate_bleu_score(
        [generated_summary],
        [[reference_summary]]
    )
    
    print_bleu_score(bleu_score)
    
    return {
        'rouge': rouge_scores,
        'bleu': bleu_score
    }


def extractive_vs_abstractive_comparison() -> None:
    """
    Explain extractive vs abstractive summarization.
    """
    logger.info("\n" + "=" * 80)
    logger.info("EXTRACTIVE VS ABSTRACTIVE SUMMARIZATION")
    logger.info("=" * 80)
    
    comparison = """
    Extractive Summarization:
    - Selects important sentences from the original text
    - Preserves exact wording from source
    - Simpler, faster, more reliable
    - May lack coherence between selected sentences
    - Examples: TextRank, LexRank
    
    Abstractive Summarization:
    - Generates new sentences that capture key ideas
    - Can paraphrase and use different words
    - More human-like, potentially more coherent
    - Requires more sophisticated models (transformers)
    - May introduce factual errors
    - Examples: BART, T5, Pegasus
    
    This demo uses: Abstractive (DistilBART)
    """
    
    logger.info(comparison)


def main():
    """Main demonstration function."""
    parser = argparse.ArgumentParser(description='Text Summarization Demo')
    parser.add_argument(
        '--text_file',
        type=str,
        default=None,
        help='Path to text file to summarize'
    )
    parser.add_argument(
        '--reference_summary',
        type=str,
        default=None,
        help='Optional reference summary for evaluation'
    )
    args = parser.parse_args()
    
    logger.info("=" * 80)
    logger.info("DAY 3: TEXT SUMMARIZATION WITH TRANSFORMERS")
    logger.info("=" * 80)
    
    # Load article
    if args.text_file and Path(args.text_file).exists():
        article = load_article(args.text_file)
    else:
        # Default article
        article_path = Path(__file__).parent.parent / "data" / "samples" / "article.txt"
        if article_path.exists():
            article = load_article(str(article_path))
        else:
            article = """
            Artificial intelligence has made significant progress in recent years. Machine learning
            algorithms can now perform tasks that were once thought to be exclusively human, such as
            image recognition, natural language processing, and game playing. Deep learning, a subset
            of machine learning, has been particularly successful. It uses neural networks with many
            layers to learn hierarchical representations of data. This has led to breakthroughs in
            computer vision, speech recognition, and language translation. However, challenges remain,
            including the need for large amounts of training data, computational resources, and
            concerns about bias and fairness in AI systems.
            """
    
    # Create summarizer
    summarizer = create_summarizer("sshleifer/distilbart-cnn-6-6")
    
    # Generate summary
    summary = generate_summary(summarizer, article, max_length=130, min_length=30)
    
    # Demonstrate different lengths
    summaries = demonstrate_different_lengths(summarizer, article)
    
    # Evaluate if reference provided
    if args.reference_summary:
        evaluate_summary(summary, args.reference_summary)
    else:
        # Use a simple reference for demo
        reference = "AI has advanced significantly with machine learning and deep learning achieving breakthroughs in various fields, though challenges like data requirements and bias remain."
        evaluate_summary(summary, reference)
    
    # Explain extractive vs abstractive
    extractive_vs_abstractive_comparison()
    
    # Save summary
    output_dir = Path(__file__).parent.parent / "examples" / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    summary_file = output_dir / "generated_summary.txt"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(f"Original Article:\n{article}\n\n")
        f.write(f"Generated Summary:\n{summary}\n")
    
    logger.info(f"\nSummary saved to: {summary_file}")
    
    logger.info("\n" + "=" * 80)
    logger.info("DEMO COMPLETE")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
