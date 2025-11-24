"""
Unit tests for evaluation metrics.

Tests classification metrics, ROUGE, and BLEU calculations.
"""

import pytest
import numpy as np
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from utils.metrics import (
    calculate_classification_metrics,
    calculate_rouge_scores,
    calculate_bleu_score
)


class TestClassificationMetrics:
    """Test classification metrics."""
    
    def test_perfect_accuracy(self):
        """Test perfect classification."""
        y_true = [0, 1, 2, 0, 1, 2]
        y_pred = [0, 1, 2, 0, 1, 2]
        
        metrics = calculate_classification_metrics(y_true, y_pred)
        
        assert metrics["accuracy"] == 1.0
        assert metrics["f1"] == 1.0
    
    def test_zero_accuracy(self):
        """Test completely wrong classification."""
        y_true = [0, 0, 0, 0]
        y_pred = [1, 1, 1, 1]
        
        metrics = calculate_classification_metrics(y_true, y_pred)
        
        assert metrics["accuracy"] == 0.0
    
    def test_partial_accuracy(self):
        """Test partial accuracy."""
        y_true = [0, 1, 0, 1]
        y_pred = [0, 1, 1, 0]
        
        metrics = calculate_classification_metrics(y_true, y_pred)
        
        assert 0 < metrics["accuracy"] < 1


class TestROUGEScores:
    """Test ROUGE score calculation."""
    
    def test_identical_texts(self):
        """Test ROUGE with identical texts."""
        predictions = ["the cat sat on the mat"]
        references = ["the cat sat on the mat"]
        
        scores = calculate_rouge_scores(predictions, references)
        
        assert "rouge1" in scores
        assert "rouge2" in scores
        assert "rougeL" in scores
        
        # Perfect match should have high scores
        assert scores["rouge1"]["fmeasure"] > 0.9
    
    def test_different_texts(self):
        """Test ROUGE with different texts."""
        predictions = ["the dog played"]
        references = ["the cat sat"]
        
        scores = calculate_rouge_scores(predictions, references)
        
        # Different texts should have lower scores
        assert scores["rouge1"]["fmeasure"] < 1.0
    
    def test_batch_processing(self):
        """Test ROUGE with multiple texts."""
        predictions = ["text one", "text two"]
        references = ["text one", "text two"]
        
        scores = calculate_rouge_scores(predictions, references)
        
        assert all(key in scores for key in ["rouge1", "rouge2", "rougeL"])


class TestBLEUScore:
    """Test BLEU score calculation."""
    
    def test_identical_texts(self):
        """Test BLEU with identical texts."""
        predictions = ["the cat sat on the mat"]
        references = [["the cat sat on the mat"]]
        
        score = calculate_bleu_score(predictions, references)
        
        assert "score" in score
        assert score["score"] > 90  # Should be very high
    
    def test_different_texts(self):
        """Test BLEU with different texts."""
        predictions = ["the dog"]
        references = [["the cat"]]
        
        score = calculate_bleu_score(predictions, references)
        
        assert score["score"] < 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
