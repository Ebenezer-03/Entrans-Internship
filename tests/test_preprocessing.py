"""
Unit tests for preprocessing utilities.

Tests text cleaning, tokenization, and preprocessing functions.
"""

import pytest
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from utils.preprocessing import (
    TextPreprocessor,
    simple_tokenize,
    remove_stopwords_from_tokens,
    get_sentence_length_stats
)


class TestTextPreprocessor:
    """Test TextPreprocessor class."""
    
    def test_lowercase(self):
        """Test lowercase conversion."""
        preprocessor = TextPreprocessor(lowercase=True, remove_punctuation=False)
        result = preprocessor.clean_text("Hello WORLD!")
        assert result == "hello world!"
    
    def test_remove_punctuation(self):
        """Test punctuation removal."""
        preprocessor = TextPreprocessor(lowercase=False, remove_punctuation=True)
        result = preprocessor.clean_text("Hello, World!")
        assert "," not in result
        assert "!" not in result
    
    def test_remove_urls(self):
        """Test URL removal."""
        preprocessor = TextPreprocessor()
        result = preprocessor.clean_text("Check out https://example.com for more info")
        assert "https://example.com" not in result
    
    def test_remove_emails(self):
        """Test email removal."""
        preprocessor = TextPreprocessor()
        result = preprocessor.clean_text("Contact us at support@example.com")
        assert "support@example.com" not in result
    
    def test_remove_numbers(self):
        """Test number removal."""
        preprocessor = TextPreprocessor(remove_numbers=True)
        result = preprocessor.clean_text("There are 123 apples")
        assert "123" not in result
    
    def test_clean_texts_batch(self):
        """Test batch text cleaning."""
        preprocessor = TextPreprocessor()
        texts = ["Hello World!", "Test TEXT"]
        results = preprocessor.clean_texts(texts)
        assert len(results) == 2
        assert all(isinstance(r, str) for r in results)


class TestSimpleTokenize:
    """Test simple tokenization."""
    
    def test_basic_tokenization(self):
        """Test basic tokenization."""
        tokens = simple_tokenize("Hello world")
        assert tokens == ["hello", "world"]
    
    def test_punctuation_handling(self):
        """Test punctuation in tokenization."""
        tokens = simple_tokenize("Hello, world!")
        assert "," in tokens or "world" in tokens


class TestStopwordRemoval:
    """Test stopword removal."""
    
    def test_remove_common_stopwords(self):
        """Test removal of common stopwords."""
        tokens = ["the", "cat", "is", "on", "mat"]
        filtered = remove_stopwords_from_tokens(tokens)
        assert "the" not in filtered
        assert "is" not in filtered
        assert "cat" in filtered
        assert "mat" in filtered


class TestSentenceLengthStats:
    """Test sentence length statistics."""
    
    def test_stats_calculation(self):
        """Test statistics calculation."""
        texts = ["short", "medium length text", "this is a longer sentence"]
        stats = get_sentence_length_stats(texts)
        
        assert "min" in stats
        assert "max" in stats
        assert "mean" in stats
        assert "median" in stats
        assert stats["min"] == 1
        assert stats["max"] == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
