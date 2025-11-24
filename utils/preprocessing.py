"""
Text Preprocessing Utilities

Provides reusable text cleaning and preprocessing functions used across
all NLP/NLU modules.

Author: NLP/NLU 3-Day Project
"""

import re
import string
from typing import List, Optional

import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download NLTK data if needed
try:
    stopwords.words("english")
except LookupError:
    import nltk
    nltk.download("stopwords", quiet=True)
    nltk.download("punkt", quiet=True)


class TextPreprocessor:
    """Text preprocessing pipeline with configurable steps."""
    
    def __init__(
        self,
        lowercase: bool = True,
        remove_punctuation: bool = True,
        remove_stopwords: bool = False,
        remove_numbers: bool = False,
        lemmatize: bool = False,
        spacy_model: str = "en_core_web_sm"
    ):
        """
        Initialize preprocessor.
        
        Args:
            lowercase: Convert text to lowercase
            remove_punctuation: Remove punctuation marks
            remove_stopwords: Remove English stopwords
            remove_numbers: Remove numeric characters
            lemmatize: Apply lemmatization (requires spaCy)
            spacy_model: spaCy model name for lemmatization
        """
        self.lowercase = lowercase
        self.remove_punctuation = remove_punctuation
        self.remove_stopwords = remove_stopwords
        self.remove_numbers = remove_numbers
        self.lemmatize = lemmatize
        
        self.stopwords_set = set(stopwords.words("english"))
        
        if self.lemmatize:
            try:
                self.nlp = spacy.load(spacy_model, disable=["parser", "ner"])
            except OSError:
                print(f"Warning: {spacy_model} not found. Lemmatization disabled.")
                self.lemmatize = False
    
    def clean_text(self, text: str) -> str:
        """
        Apply all preprocessing steps to text.
        
        Args:
            text: Input text string
            
        Returns:
            Cleaned text string
        """
        if not text or not isinstance(text, str):
            return ""
        
        # Lowercase
        if self.lowercase:
            text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove numbers
        if self.remove_numbers:
            text = re.sub(r'\d+', '', text)
        
        # Remove punctuation
        if self.remove_punctuation:
            text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Lemmatization
        if self.lemmatize:
            doc = self.nlp(text)
            text = ' '.join([token.lemma_ for token in doc])
        
        # Remove stopwords (after lemmatization)
        if self.remove_stopwords:
            tokens = text.split()
            tokens = [t for t in tokens if t not in self.stopwords_set]
            text = ' '.join(tokens)
        
        return text
    
    def clean_texts(self, texts: List[str]) -> List[str]:
        """
        Clean a list of texts.
        
        Args:
            texts: List of text strings
            
        Returns:
            List of cleaned text strings
        """
        return [self.clean_text(text) for text in texts]


def simple_tokenize(text: str, lowercase: bool = True) -> List[str]:
    """
    Simple word tokenization.
    
    Args:
        text: Input text
        lowercase: Convert to lowercase
        
    Returns:
        List of tokens
    """
    if lowercase:
        text = text.lower()
    return word_tokenize(text)


def remove_stopwords_from_tokens(tokens: List[str]) -> List[str]:
    """
    Remove stopwords from token list.
    
    Args:
        tokens: List of tokens
        
    Returns:
        Filtered token list
    """
    stop_words = set(stopwords.words("english"))
    return [token for token in tokens if token not in stop_words]


def get_sentence_length_stats(texts: List[str]) -> dict:
    """
    Calculate sentence length statistics.
    
    Args:
        texts: List of text strings
        
    Returns:
        Dictionary with min, max, mean, median lengths
    """
    import numpy as np
    
    lengths = [len(text.split()) for text in texts]
    
    return {
        "min": min(lengths),
        "max": max(lengths),
        "mean": np.mean(lengths),
        "median": np.median(lengths),
        "std": np.std(lengths)
    }


if __name__ == "__main__":
    # Example usage
    sample_texts = [
        "This is a SAMPLE text with URLs like https://example.com!",
        "Another example with email@example.com and numbers 12345.",
        "Testing preprocessing pipeline with stopwords and punctuation!!!"
    ]
    
    preprocessor = TextPreprocessor(
        lowercase=True,
        remove_punctuation=True,
        remove_stopwords=True,
        lemmatize=True
    )
    
    print("Original texts:")
    for text in sample_texts:
        print(f"  - {text}")
    
    print("\nCleaned texts:")
    cleaned = preprocessor.clean_texts(sample_texts)
    for text in cleaned:
        print(f"  - {text}")
    
    print("\nLength statistics:")
    stats = get_sentence_length_stats(sample_texts)
    for key, value in stats.items():
        print(f"  {key}: {value:.2f}")
