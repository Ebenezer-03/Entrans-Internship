"""
Day 1: Tokenization and Lemmatization with spaCy

Demonstrates:
- Loading spaCy models
- Tokenization and sentence segmentation
- Stopword filtering
- Lemmatization vs stemming
- Part-of-speech tagging
- Token attributes

Expected Runtime: ~30 seconds (CPU)
Input: Text strings
Output: Tokens, lemmas, POS tags, linguistic features

Author: NLP/NLU 3-Day Project
"""

import logging
from pathlib import Path
from typing import List, Dict
import spacy
from spacy.tokens import Doc

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_spacy_model(model_name: str = "en_core_web_sm") -> spacy.Language:
    """
    Load spaCy language model.
    
    Args:
        model_name: spaCy model name
        
    Returns:
        Loaded spaCy nlp object
    """
    try:
        nlp = spacy.load(model_name)
        logger.info(f"Loaded spaCy model: {model_name}")
        return nlp
    except OSError:
        logger.error(f"Model '{model_name}' not found. Please run: python -m spacy download {model_name}")
        raise


def demonstrate_tokenization(nlp: spacy.Language, text: str) -> None:
    """
    Demonstrate basic tokenization.
    
    Args:
        nlp: spaCy nlp object
        text: Input text
    """
    logger.info("\n" + "=" * 80)
    logger.info("TOKENIZATION DEMO")
    logger.info("=" * 80)
    
    doc = nlp(text)
    
    logger.info(f"\nOriginal text:\n  {text}")
    logger.info(f"\nNumber of tokens: {len(doc)}")
    logger.info("\nTokens:")
    for i, token in enumerate(doc, 1):
        logger.info(f"  {i:2d}. '{token.text}' (is_alpha={token.is_alpha}, is_punct={token.is_punct})")


def demonstrate_sentence_segmentation(nlp: spacy.Language, text: str) -> None:
    """
    Demonstrate sentence segmentation.
    
    Args:
        nlp: spaCy nlp object
        text: Input text with multiple sentences
    """
    logger.info("\n" + "=" * 80)
    logger.info("SENTENCE SEGMENTATION DEMO")
    logger.info("=" * 80)
    
    doc = nlp(text)
    
    logger.info(f"\nNumber of sentences: {len(list(doc.sents))}")
    logger.info("\nSentences:")
    for i, sent in enumerate(doc.sents, 1):
        logger.info(f"  {i}. {sent.text}")


def demonstrate_stopwords(nlp: spacy.Language, text: str) -> None:
    """
    Demonstrate stopword filtering.
    
    Args:
        nlp: spaCy nlp object
        text: Input text
    """
    logger.info("\n" + "=" * 80)
    logger.info("STOPWORD FILTERING DEMO")
    logger.info("=" * 80)
    
    doc = nlp(text)
    
    stopwords = [token for token in doc if token.is_stop]
    content_words = [token for token in doc if not token.is_stop and token.is_alpha]
    
    logger.info(f"\nTotal tokens: {len(doc)}")
    logger.info(f"Stopwords: {len(stopwords)}")
    logger.info(f"Content words: {len(content_words)}")
    
    logger.info(f"\nStopwords found: {[t.text for t in stopwords]}")
    logger.info(f"\nContent words: {[t.text for t in content_words]}")


def demonstrate_lemmatization(nlp: spacy.Language, text: str) -> None:
    """
    Demonstrate lemmatization.
    
    Args:
        nlp: spaCy nlp object
        text: Input text
    """
    logger.info("\n" + "=" * 80)
    logger.info("LEMMATIZATION DEMO")
    logger.info("=" * 80)
    
    doc = nlp(text)
    
    logger.info("\nToken -> Lemma:")
    for token in doc:
        if token.is_alpha:
            logger.info(f"  {token.text:15s} -> {token.lemma_:15s} (POS: {token.pos_})")


def demonstrate_pos_tagging(nlp: spacy.Language, text: str) -> None:
    """
    Demonstrate part-of-speech tagging.
    
    Args:
        nlp: spaCy nlp object
        text: Input text
    """
    logger.info("\n" + "=" * 80)
    logger.info("PART-OF-SPEECH TAGGING DEMO")
    logger.info("=" * 80)
    
    doc = nlp(text)
    
    logger.info("\nToken | Lemma | POS | Tag | Dependency")
    logger.info("-" * 80)
    for token in doc:
        logger.info(
            f"{token.text:12s} | {token.lemma_:12s} | {token.pos_:6s} | "
            f"{token.tag_:6s} | {token.dep_:10s}"
        )


def demonstrate_token_attributes(nlp: spacy.Language, text: str) -> None:
    """
    Demonstrate various token attributes.
    
    Args:
        nlp: spaCy nlp object
        text: Input text
    """
    logger.info("\n" + "=" * 80)
    logger.info("TOKEN ATTRIBUTES DEMO")
    logger.info("=" * 80)
    
    doc = nlp(text)
    
    logger.info("\nToken attributes:")
    for token in doc[:10]:  # First 10 tokens
        logger.info(f"\nToken: '{token.text}'")
        logger.info(f"  - Lowercase: {token.lower_}")
        logger.info(f"  - Is alphabetic: {token.is_alpha}")
        logger.info(f"  - Is punctuation: {token.is_punct}")
        logger.info(f"  - Is digit: {token.is_digit}")
        logger.info(f"  - Is stopword: {token.is_stop}")
        logger.info(f"  - Shape: {token.shape_}")
        logger.info(f"  - Is OOV: {token.is_oov}")


def compare_stemming_lemmatization() -> None:
    """
    Compare stemming (NLTK) vs lemmatization (spaCy).
    """
    logger.info("\n" + "=" * 80)
    logger.info("STEMMING vs LEMMATIZATION COMPARISON")
    logger.info("=" * 80)
    
    from nltk.stem import PorterStemmer
    import nltk
    
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
    
    stemmer = PorterStemmer()
    nlp = load_spacy_model()
    
    test_words = [
        "running", "ran", "runs",
        "better", "best", "good",
        "studies", "studying", "studied",
        "feet", "foot",
        "geese", "goose"
    ]
    
    logger.info("\nWord -> Stemmed (Porter) | Lemmatized (spaCy)")
    logger.info("-" * 60)
    
    for word in test_words:
        stemmed = stemmer.stem(word)
        doc = nlp(word)
        lemmatized = doc[0].lemma_
        logger.info(f"{word:12s} -> {stemmed:12s} | {lemmatized:12s}")


def main():
    """Main demonstration function."""
    logger.info("=" * 80)
    logger.info("DAY 1: TOKENIZATION AND LEMMATIZATION WITH SPACY")
    logger.info("=" * 80)
    
    # Load spaCy model
    nlp = load_spacy_model("en_core_web_sm")
    
    # Sample texts
    simple_text = "The quick brown fox jumps over the lazy dog."
    
    multi_sentence = (
        "Natural language processing is fascinating! "
        "It enables computers to understand human language. "
        "SpaCy makes NLP easy and efficient."
    )
    
    complex_text = (
        "The researchers are studying the effects of climate change. "
        "They have been analyzing data for several years. "
        "Their findings will be published next month."
    )
    
    # Run demonstrations
    demonstrate_tokenization(nlp, simple_text)
    demonstrate_sentence_segmentation(nlp, multi_sentence)
    demonstrate_stopwords(nlp, simple_text)
    demonstrate_lemmatization(nlp, complex_text)
    demonstrate_pos_tagging(nlp, simple_text)
    demonstrate_token_attributes(nlp, simple_text)
    compare_stemming_lemmatization()
    
    logger.info("\n" + "=" * 80)
    logger.info("DEMO COMPLETE")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
