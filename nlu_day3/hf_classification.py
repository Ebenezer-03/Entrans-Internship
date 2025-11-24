"""
Day 3: HuggingFace Transformers Classification

Demonstrates:
- Fine-tuning DistilBERT for sentiment/topic classification
- Using HuggingFace Trainer API
- Evaluation with metrics
- Model checkpoint saving

Expected Runtime: ~3 minutes (CPU, 1 epoch, 200 samples)
Input: Sentiment or topic dataset
Output: Fine-tuned model, evaluation metrics

Author: NLP/NLU 3-Day Project
Usage:
    python hf_classification.py --task sentiment --epochs 1 --subset 200
    python hf_classification.py --task topic --epochs 3 --subset 500
"""

import argparse
import logging
from pathlib import Path
from typing import Dict
import numpy as np
import pandas as pd
import torch
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    EvalPrediction
)
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_dataset_for_task(task: str, subset_size: int = None) -> tuple:
    """
    Load dataset for specified task.
    
    Args:
        task: 'sentiment' or 'topic'
        subset_size: Optional subset size for quick demos
        
    Returns:
        Tuple of (texts, labels, num_labels, label_names)
    """
    data_dir = Path(__file__).parent.parent / "data" / "samples"
    
    if task == "sentiment":
        data_path = data_dir / "sentiment_small.csv"
        num_labels = 2
        label_names = ["Negative", "Positive"]
    elif task == "topic":
        data_path = data_dir / "topics_small.csv"
        num_labels = 4
        label_names = ["World", "Sports", "Business", "Sci/Tech"]
    else:
        raise ValueError(f"Unknown task: {task}")
    
    logger.info(f"\nLoading {task} dataset from {data_path}")
    
    if not data_path.exists():
        raise FileNotFoundError(f"Dataset not found: {data_path}")
    
    df = pd.read_csv(data_path)
    
    # Subset if requested
    if subset_size and subset_size < len(df):
        df = df.sample(n=subset_size, random_state=42)
        logger.info(f"Using subset of {subset_size} samples")
    
    texts = df['text'].tolist()
    labels = df['label'].tolist()
    
    logger.info(f"Loaded {len(texts)} samples with {num_labels} classes")
    
    return texts, labels, num_labels, label_names


def prepare_datasets(texts: list, labels: list, tokenizer, test_size: float = 0.2):
    """
    Prepare train and test datasets.
    
    Args:
        texts: List of texts
        labels: List of labels
        tokenizer: HuggingFace tokenizer
        test_size: Test set proportion
        
    Returns:
        Tuple of (train_dataset, test_dataset)
    """
    logger.info("\nPreparing datasets...")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=test_size, random_state=42, stratify=labels
    )
    
    logger.info(f"  Train samples: {len(X_train)}")
    logger.info(f"  Test samples: {len(X_test)}")
    
    # Create datasets
    train_data = {"text": X_train, "label": y_train}
    test_data = {"text": X_test, "label": y_test}
    
    train_dataset = Dataset.from_dict(train_data)
    test_dataset = Dataset.from_dict(test_data)
    
    # Tokenize
    def tokenize_function(examples):
        return tokenizer(
            examples["text"],
            padding="max_length",
            truncation=True,
            max_length=256
        )
    
    logger.info("Tokenizing datasets...")
    train_dataset = train_dataset.map(tokenize_function, batched=True)
    test_dataset = test_dataset.map(tokenize_function, batched=True)
    
    return train_dataset, test_dataset


def compute_metrics(pred: EvalPrediction) -> Dict[str, float]:
    """
    Compute evaluation metrics.
    
    Args:
        pred: EvalPrediction object
        
    Returns:
        Dictionary of metrics
    """
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, preds, average='weighted', zero_division=0
    )
    acc = accuracy_score(labels, preds)
    
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }


def train_classifier(
    train_dataset,
    test_dataset,
    num_labels: int,
    model_name: str = "distilbert-base-uncased",
    num_epochs: int = 3,
    batch_size: int = 16,
    learning_rate: float = 2e-5
) -> Trainer:
    """
    Train classifier using HuggingFace Trainer.
    
    Args:
        train_dataset: Training dataset
        test_dataset: Test dataset
        num_labels: Number of classes
        model_name: Pre-trained model name
        num_epochs: Number of training epochs
        batch_size: Batch size
        learning_rate: Learning rate
        
    Returns:
        Trained Trainer object
    """
    logger.info("\n" + "=" * 80)
    logger.info("TRAINING HUGGINGFACE TRANSFORMER CLASSIFIER")
    logger.info("=" * 80)
    
    logger.info(f"\nModel: {model_name}")
    logger.info(f"Epochs: {num_epochs}")
    logger.info(f"Batch size: {batch_size}")
    logger.info(f"Learning rate: {learning_rate}")
    
    # Load model
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        num_labels=num_labels
    )
    
    # Training arguments
    output_dir = Path(__file__).parent.parent / "examples" / "outputs" / "hf_classifier"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    training_args = TrainingArguments(
        output_dir=str(output_dir),
        num_train_epochs=num_epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        learning_rate=learning_rate,
        weight_decay=0.01,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        logging_dir=str(output_dir / "logs"),
        logging_steps=10,
        report_to="none"  # Disable wandb
    )
    
    # Create trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
        compute_metrics=compute_metrics
    )
    
    # Train
    logger.info("\nStarting training...")
    trainer.train()
    
    # Evaluate
    logger.info("\nEvaluating on test set...")
    metrics = trainer.evaluate()
    
    logger.info("\nTest Set Performance:")
    logger.info(f"  Accuracy:  {metrics['eval_accuracy']:.4f}")
    logger.info(f"  F1 Score:  {metrics['eval_f1']:.4f}")
    logger.info(f"  Precision: {metrics['eval_precision']:.4f}")
    logger.info(f"  Recall:    {metrics['eval_recall']:.4f}")
    
    # Save model
    model_save_path = output_dir / "final_model"
    trainer.save_model(str(model_save_path))
    logger.info(f"\nModel saved to: {model_save_path}")
    
    return trainer


def predict_examples(trainer: Trainer, tokenizer, examples: list, label_names: list) -> None:
    """
    Predict on example texts.
    
    Args:
        trainer: Trained Trainer object
        tokenizer: Tokenizer
        examples: Example texts
        label_names: Label names
    """
    logger.info("\n" + "=" * 80)
    logger.info("PREDICTION EXAMPLES")
    logger.info("=" * 80)
    
    for text in examples:
        # Tokenize
        inputs = tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=256
        )
        
        # Predict
        with torch.no_grad():
            outputs = trainer.model(**inputs)
            logits = outputs.logits
            pred = logits.argmax(-1).item()
        
        logger.info(f"\nText: {text}")
        logger.info(f"Predicted: {label_names[pred]}")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='HuggingFace Classification Demo')
    parser.add_argument(
        '--task',
        type=str,
        default='sentiment',
        choices=['sentiment', 'topic'],
        help='Classification task'
    )
    parser.add_argument(
        '--epochs',
        type=int,
        default=1,
        help='Number of training epochs'
    )
    parser.add_argument(
        '--subset',
        type=int,
        default=200,
        help='Subset size for quick demo'
    )
    parser.add_argument(
        '--batch_size',
        type=int,
        default=16,
        help='Batch size'
    )
    args = parser.parse_args()
    
    logger.info("=" * 80)
    logger.info("DAY 3: HUGGINGFACE TRANSFORMERS CLASSIFICATION")
    logger.info("=" * 80)
    
    # Load data
    texts, labels, num_labels, label_names = load_dataset_for_task(
        args.task,
        subset_size=args.subset
    )
    
    # Load tokenizer
    model_name = "distilbert-base-uncased"
    logger.info(f"\nLoading tokenizer: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Prepare datasets
    train_dataset, test_dataset = prepare_datasets(texts, labels, tokenizer)
    
    # Train classifier
    trainer = train_classifier(
        train_dataset,
        test_dataset,
        num_labels=num_labels,
        model_name=model_name,
        num_epochs=args.epochs,
        batch_size=args.batch_size
    )
    
    # Predict on examples
    if args.task == "sentiment":
        examples = [
            "This movie was absolutely amazing! Best film I've seen this year.",
            "Terrible waste of time. I want my money back.",
            "It was okay, nothing special but not bad either."
        ]
    else:  # topic
        examples = [
            "The Federal Reserve announced new interest rate policies today.",
            "NASA successfully launched the new Mars rover mission.",
            "The championship game drew a record-breaking crowd."
        ]
    
    predict_examples(trainer, tokenizer, examples, label_names)
    
    logger.info("\n" + "=" * 80)
    logger.info("DEMO COMPLETE")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
