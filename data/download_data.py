"""
Data Download and Preparation Script

Downloads and prepares small sample datasets for NLP/NLU demos:
- IMDB sentiment subset
- AG News topic classification subset
- CNN/DailyMail summarization excerpt
- Custom NER examples

Author: NLP/NLU 3-Day Project
"""

import os
import csv
import random
from pathlib import Path
from typing import List, Tuple
import logging

import pandas as pd
from datasets import load_dataset

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set random seed for reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

# Paths
BASE_DIR = Path(__file__).parent
SAMPLES_DIR = BASE_DIR / "samples"
DOWNLOADS_DIR = BASE_DIR / "downloads"

# Create directories
SAMPLES_DIR.mkdir(exist_ok=True)
DOWNLOADS_DIR.mkdir(exist_ok=True)


def download_imdb_sentiment(num_samples: int = 500) -> None:
    """
    Download IMDB sentiment dataset subset.
    
    Args:
        num_samples: Number of samples to download (balanced)
    """
    logger.info(f"Downloading IMDB sentiment dataset ({num_samples} samples)...")
    
    try:
        # Load dataset from HuggingFace
        dataset = load_dataset("imdb", split="train")
        
        # Sample balanced subset
        df = pd.DataFrame(dataset)
        df_pos = df[df['label'] == 1].sample(n=num_samples // 2, random_state=RANDOM_SEED)
        df_neg = df[df['label'] == 0].sample(n=num_samples // 2, random_state=RANDOM_SEED)
        df_sample = pd.concat([df_pos, df_neg]).sample(frac=1, random_state=RANDOM_SEED)
        
        # Save to CSV
        output_path = SAMPLES_DIR / "sentiment_small.csv"
        df_sample[['text', 'label']].to_csv(output_path, index=False)
        
        logger.info(f"Saved {len(df_sample)} samples to {output_path}")
        logger.info(f"  Positive: {(df_sample['label'] == 1).sum()}")
        logger.info(f"  Negative: {(df_sample['label'] == 0).sum()}")
        
    except Exception as e:
        logger.error(f"Error downloading IMDB dataset: {e}")
        logger.info("Creating fallback sample data...")
        create_fallback_sentiment_data()


def download_ag_news(num_samples: int = 1000) -> None:
    """
    Download AG News topic classification dataset subset.
    
    Args:
        num_samples: Number of samples to download (balanced across classes)
    """
    logger.info(f"Downloading AG News dataset ({num_samples} samples)...")
    
    try:
        # Load dataset from HuggingFace
        dataset = load_dataset("ag_news", split="train")
        
        # Sample balanced subset
        df = pd.DataFrame(dataset)
        samples_per_class = num_samples // 4
        
        dfs = []
        for label in range(4):
            df_class = df[df['label'] == label].sample(
                n=samples_per_class,
                random_state=RANDOM_SEED
            )
            dfs.append(df_class)
        
        df_sample = pd.concat(dfs).sample(frac=1, random_state=RANDOM_SEED)
        
        # Save to CSV
        output_path = SAMPLES_DIR / "topics_small.csv"
        df_sample[['text', 'label']].to_csv(output_path, index=False)
        
        logger.info(f"Saved {len(df_sample)} samples to {output_path}")
        for label in range(4):
            count = (df_sample['label'] == label).sum()
            logger.info(f"  Class {label}: {count}")
        
    except Exception as e:
        logger.error(f"Error downloading AG News dataset: {e}")
        logger.info("Creating fallback sample data...")
        create_fallback_topics_data()


def download_cnn_dailymail(num_samples: int = 50) -> None:
    """
    Download CNN/DailyMail summarization dataset excerpt.
    
    Args:
        num_samples: Number of article-summary pairs
    """
    logger.info(f"Downloading CNN/DailyMail dataset ({num_samples} samples)...")
    
    try:
        # Load dataset from HuggingFace
        dataset = load_dataset("cnn_dailymail", "3.0.0", split="train")
        
        # Sample subset
        indices = random.sample(range(len(dataset)), num_samples)
        samples = [dataset[i] for i in indices]
        
        # Save to CSV
        output_path = SAMPLES_DIR / "summarization_small.csv"
        df = pd.DataFrame({
            'article': [s['article'] for s in samples],
            'highlights': [s['highlights'] for s in samples]
        })
        df.to_csv(output_path, index=False)
        
        logger.info(f"Saved {len(df)} samples to {output_path}")
        
        # Save one article as example
        article_path = SAMPLES_DIR / "article.txt"
        with open(article_path, 'w', encoding='utf-8') as f:
            f.write(samples[0]['article'])
        logger.info(f"Saved example article to {article_path}")
        
    except Exception as e:
        logger.error(f"Error downloading CNN/DailyMail dataset: {e}")
        logger.info("Creating fallback sample data...")
        create_fallback_summarization_data()


def create_ner_examples() -> None:
    """Create sample texts for NER demonstration."""
    logger.info("Creating NER example texts...")
    
    examples = [
        "Apple Inc. is planning to open a new store in New York City next month.",
        "Elon Musk announced on Twitter that Tesla will release a new model in 2024.",
        "The meeting is scheduled for January 15th at 3:00 PM in the conference room.",
        "Dr. Sarah Johnson from Stanford University published a groundbreaking paper.",
        "Amazon CEO Jeff Bezos visited the Seattle headquarters last Tuesday.",
        "The European Union imposed new regulations on tech companies like Google and Facebook.",
        "Barack Obama gave a speech at the United Nations in Geneva, Switzerland.",
        "Microsoft acquired GitHub for $7.5 billion in June 2018.",
        "The World Health Organization (WHO) is based in Geneva and has 194 member states.",
        "Professor Alan Turing worked at Bletchley Park during World War II."
    ]
    
    output_path = SAMPLES_DIR / "ner_examples.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(examples))
    
    logger.info(f"Saved {len(examples)} NER examples to {output_path}")


def create_fallback_sentiment_data() -> None:
    """Create minimal fallback sentiment data if download fails."""
    data = {
        'text': [
            "This movie was absolutely fantastic! I loved every minute of it.",
            "Terrible film, waste of time and money.",
            "Great acting and beautiful cinematography.",
            "Boring and predictable plot.",
            "One of the best movies I've ever seen!",
            "Disappointing and poorly executed."
        ] * 50,  # Repeat to get 300 samples
        'label': [1, 0, 1, 0, 1, 0] * 50
    }
    
    df = pd.DataFrame(data)
    output_path = SAMPLES_DIR / "sentiment_small.csv"
    df.to_csv(output_path, index=False)
    logger.info(f"Created fallback sentiment data: {output_path}")


def create_fallback_topics_data() -> None:
    """Create minimal fallback topic data if download fails."""
    data = {
        'text': [
            "The stock market reached new highs today.",  # Business
            "Scientists discover new planet in distant galaxy.",  # Sci/Tech
            "Local team wins championship game.",  # Sports
            "New policy announced by government officials.",  # World
        ] * 75,  # Repeat to get 300 samples
        'label': [0, 1, 2, 3] * 75
    }
    
    df = pd.DataFrame(data)
    output_path = SAMPLES_DIR / "topics_small.csv"
    df.to_csv(output_path, index=False)
    logger.info(f"Created fallback topics data: {output_path}")


def create_fallback_summarization_data() -> None:
    """Create minimal fallback summarization data if download fails."""
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
    
    summary = "AI has advanced significantly with machine learning and deep learning achieving breakthroughs in various fields, though challenges like data requirements and bias remain."
    
    # Save article
    article_path = SAMPLES_DIR / "article.txt"
    with open(article_path, 'w', encoding='utf-8') as f:
        f.write(article.strip())
    
    # Save CSV
    df = pd.DataFrame({'article': [article.strip()], 'highlights': [summary]})
    output_path = SAMPLES_DIR / "summarization_small.csv"
    df.to_csv(output_path, index=False)
    
    logger.info(f"Created fallback summarization data: {output_path}")


def main():
    """Download all datasets."""
    logger.info("Starting data download process...")
    logger.info(f"Random seed: {RANDOM_SEED}")
    logger.info(f"Output directory: {SAMPLES_DIR}")
    
    # Download datasets
    download_imdb_sentiment(num_samples=500)
    download_ag_news(num_samples=1000)
    download_cnn_dailymail(num_samples=50)
    create_ner_examples()
    
    logger.info("\nData download complete!")
    logger.info(f"All files saved to: {SAMPLES_DIR}")
    
    # List created files
    logger.info("\nCreated files:")
    for file in sorted(SAMPLES_DIR.glob("*")):
        size_kb = file.stat().st_size / 1024
        logger.info(f"  - {file.name} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
