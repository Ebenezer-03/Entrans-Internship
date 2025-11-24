"""
Day 1: Named Entity Recognition and Rule-Based Matching with spaCy

Demonstrates:
- Named Entity Recognition (NER)
- Entity visualization
- Rule-based pattern matching (Matcher)
- Phrase matching (PhraseMatcher)
- Custom entity extraction patterns

Expected Runtime: ~30 seconds (CPU)
Input: Text with entities
Output: Extracted entities, matched patterns

Author: NLP/NLU 3-Day Project
"""

import logging
from pathlib import Path
from typing import List, Tuple
import spacy
from spacy import displacy
from spacy.matcher import Matcher, PhraseMatcher
from spacy.tokens import Span

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_ner_examples() -> List[str]:
    """
    Load NER example texts.
    
    Returns:
        List of example texts
    """
    examples_path = Path(__file__).parent.parent / "data" / "samples" / "ner_examples.txt"
    
    if examples_path.exists():
        with open(examples_path, 'r', encoding='utf-8') as f:
            examples = [line.strip() for line in f if line.strip()]
        logger.info(f"Loaded {len(examples)} examples from {examples_path}")
        return examples
    else:
        logger.warning(f"Examples file not found: {examples_path}")
        return [
            "Apple Inc. is planning to open a new store in New York City next month.",
            "Elon Musk announced on Twitter that Tesla will release a new model in 2024.",
        ]


def demonstrate_ner(nlp: spacy.Language, texts: List[str]) -> None:
    """
    Demonstrate Named Entity Recognition.
    
    Args:
        nlp: spaCy nlp object
        texts: List of input texts
    """
    logger.info("\n" + "=" * 80)
    logger.info("NAMED ENTITY RECOGNITION DEMO")
    logger.info("=" * 80)
    
    for i, text in enumerate(texts, 1):
        logger.info(f"\n--- Example {i} ---")
        logger.info(f"Text: {text}")
        
        doc = nlp(text)
        
        if doc.ents:
            logger.info(f"\nFound {len(doc.ents)} entities:")
            for ent in doc.ents:
                logger.info(f"  - '{ent.text}' ({ent.label_}) - {spacy.explain(ent.label_)}")
        else:
            logger.info("  No entities found.")


def visualize_entities(nlp: spacy.Language, text: str, output_path: str = None) -> None:
    """
    Visualize entities using displacy.
    
    Args:
        nlp: spaCy nlp object
        text: Input text
        output_path: Optional path to save HTML visualization
    """
    logger.info("\n" + "=" * 80)
    logger.info("ENTITY VISUALIZATION")
    logger.info("=" * 80)
    
    doc = nlp(text)
    
    # Console visualization
    logger.info(f"\nText: {text}")
    logger.info("\nEntities (with context):")
    for ent in doc.ents:
        start = max(0, ent.start_char - 20)
        end = min(len(text), ent.end_char + 20)
        context = text[start:end]
        logger.info(f"  ...{context}...")
        logger.info(f"    -> {ent.text} ({ent.label_})")
    
    # HTML visualization (optional)
    if output_path:
        html = displacy.render(doc, style="ent", page=True)
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        logger.info(f"\nHTML visualization saved to: {output_path}")


def demonstrate_rule_based_matching(nlp: spacy.Language) -> None:
    """
    Demonstrate rule-based pattern matching.
    
    Args:
        nlp: spaCy nlp object
    """
    logger.info("\n" + "=" * 80)
    logger.info("RULE-BASED PATTERN MATCHING DEMO")
    logger.info("=" * 80)
    
    # Initialize matcher
    matcher = Matcher(nlp.vocab)
    
    # Pattern 1: Email addresses
    email_pattern = [
        {"LIKE_EMAIL": True}
    ]
    matcher.add("EMAIL", [email_pattern])
    
    # Pattern 2: Phone numbers (simple pattern)
    phone_pattern = [
        {"SHAPE": "ddd"},
        {"TEXT": "-"},
        {"SHAPE": "ddd"},
        {"TEXT": "-"},
        {"SHAPE": "dddd"}
    ]
    matcher.add("PHONE", [phone_pattern])
    
    # Pattern 3: Money amounts
    money_pattern = [
        {"TEXT": "$"},
        {"LIKE_NUM": True}
    ]
    matcher.add("MONEY", [money_pattern])
    
    # Pattern 4: Dates (month + day)
    date_pattern = [
        {"TEXT": {"IN": ["January", "February", "March", "April", "May", "June",
                         "July", "August", "September", "October", "November", "December"]}},
        {"LIKE_NUM": True}
    ]
    matcher.add("DATE", [date_pattern])
    
    # Test text
    test_text = (
        "Contact us at support@example.com or call 555-123-4567. "
        "The price is $99.99. Meeting scheduled for January 15th."
    )
    
    logger.info(f"\nTest text: {test_text}")
    
    doc = nlp(test_text)
    matches = matcher(doc)
    
    logger.info(f"\nFound {len(matches)} matches:")
    for match_id, start, end in matches:
        rule_name = nlp.vocab.strings[match_id]
        matched_span = doc[start:end]
        logger.info(f"  - {rule_name}: '{matched_span.text}'")


def demonstrate_phrase_matching(nlp: spacy.Language) -> None:
    """
    Demonstrate phrase matching for terminology extraction.
    
    Args:
        nlp: spaCy nlp object
    """
    logger.info("\n" + "=" * 80)
    logger.info("PHRASE MATCHING DEMO")
    logger.info("=" * 80)
    
    # Initialize phrase matcher
    phrase_matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    
    # Define terminology
    tech_terms = [
        "machine learning", "deep learning", "neural network",
        "natural language processing", "computer vision",
        "artificial intelligence", "data science"
    ]
    
    # Create patterns
    patterns = [nlp.make_doc(term) for term in tech_terms]
    phrase_matcher.add("TECH_TERMS", patterns)
    
    # Test text
    test_text = (
        "Machine Learning and Deep Learning are subfields of Artificial Intelligence. "
        "Natural Language Processing enables computers to understand human language. "
        "Computer Vision allows machines to interpret visual information."
    )
    
    logger.info(f"\nTest text: {test_text}")
    logger.info(f"\nLooking for technical terms: {tech_terms}")
    
    doc = nlp(test_text)
    matches = phrase_matcher(doc)
    
    logger.info(f"\nFound {len(matches)} matches:")
    for match_id, start, end in matches:
        matched_span = doc[start:end]
        logger.info(f"  - '{matched_span.text}'")


def extract_custom_entities(nlp: spacy.Language, text: str) -> None:
    """
    Extract custom entities using patterns.
    
    Args:
        nlp: spaCy nlp object
        text: Input text
    """
    logger.info("\n" + "=" * 80)
    logger.info("CUSTOM ENTITY EXTRACTION")
    logger.info("=" * 80)
    
    matcher = Matcher(nlp.vocab)
    
    # Pattern: Product names (capitalized words followed by version numbers)
    product_pattern = [
        {"POS": "PROPN", "OP": "+"},
        {"LIKE_NUM": True}
    ]
    matcher.add("PRODUCT", [product_pattern])
    
    # Pattern: Job titles
    job_title_pattern = [
        {"TEXT": {"IN": ["CEO", "CTO", "CFO", "Dr.", "Professor", "Manager"]}},
        {"POS": "PROPN", "OP": "*"}
    ]
    matcher.add("JOB_TITLE", [job_title_pattern])
    
    logger.info(f"\nText: {text}")
    
    doc = nlp(text)
    matches = matcher(doc)
    
    logger.info(f"\nExtracted custom entities:")
    for match_id, start, end in matches:
        entity_type = nlp.vocab.strings[match_id]
        matched_span = doc[start:end]
        logger.info(f"  - {entity_type}: '{matched_span.text}'")


def main():
    """Main demonstration function."""
    logger.info("=" * 80)
    logger.info("DAY 1: NER AND RULE-BASED MATCHING WITH SPACY")
    logger.info("=" * 80)
    
    # Load spaCy model
    try:
        nlp = spacy.load("en_core_web_sm")
        logger.info("Loaded spaCy model: en_core_web_sm")
    except OSError:
        logger.error("Model 'en_core_web_sm' not found. Please run: python -m spacy download en_core_web_sm")
        return
    
    # Load examples
    examples = load_ner_examples()
    
    # Run demonstrations
    demonstrate_ner(nlp, examples[:5])  # First 5 examples
    
    # Visualize one example
    if examples:
        output_dir = Path(__file__).parent.parent / "examples" / "outputs"
        output_dir.mkdir(parents=True, exist_ok=True)
        visualize_entities(
            nlp,
            examples[0],
            output_path=str(output_dir / "ner_visualization.html")
        )
    
    demonstrate_rule_based_matching(nlp)
    demonstrate_phrase_matching(nlp)
    
    # Custom entity extraction
    custom_text = "CEO Elon Musk announced Tesla Model 3 will be updated. Dr. Sarah Johnson leads the research."
    extract_custom_entities(nlp, custom_text)
    
    logger.info("\n" + "=" * 80)
    logger.info("DEMO COMPLETE")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
