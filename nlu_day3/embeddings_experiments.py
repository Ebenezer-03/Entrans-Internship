"""
Day 3: BERT Embeddings and Semantic Similarity

Demonstrates:
- Extracting BERT embeddings using transformers
- Cosine similarity calculation
- Semantic search examples
- Comparison: BOW vs Word2Vec vs BERT
- t-SNE visualization of embeddings

Expected Runtime: ~1 minute (CPU)
Input: Text sentences
Output: Embeddings, similarity scores, visualizations

Author: NLP/NLU 3-Day Project
"""

import logging
from pathlib import Path
from typing import List, Tuple
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import seaborn as sns

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_bert_model(model_name: str = "distilbert-base-uncased") -> Tuple:
    """
    Load BERT model and tokenizer.
    
    Args:
        model_name: HuggingFace model name
        
    Returns:
        Tuple of (tokenizer, model)
    """
    logger.info(f"\nLoading model: {model_name}")
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    
    # Set to evaluation mode
    model.eval()
    
    logger.info("Model loaded successfully")
    
    return tokenizer, model


def get_bert_embeddings(
    texts: List[str],
    tokenizer,
    model,
    pooling: str = "mean"
) -> np.ndarray:
    """
    Extract BERT embeddings for texts.
    
    Args:
        texts: List of input texts
        tokenizer: BERT tokenizer
        model: BERT model
        pooling: Pooling strategy ('mean', 'cls', 'max')
        
    Returns:
        Numpy array of embeddings (n_texts, embedding_dim)
    """
    logger.info(f"\nExtracting embeddings for {len(texts)} texts...")
    logger.info(f"Pooling strategy: {pooling}")
    
    embeddings = []
    
    with torch.no_grad():
        for text in texts:
            # Tokenize
            inputs = tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                padding=True,
                max_length=512
            )
            
            # Get model outputs
            outputs = model(**inputs)
            
            # Pool embeddings
            if pooling == "mean":
                # Mean pooling over all tokens
                embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
            elif pooling == "cls":
                # Use [CLS] token embedding
                embedding = outputs.last_hidden_state[:, 0, :].squeeze().numpy()
            elif pooling == "max":
                # Max pooling over all tokens
                embedding = outputs.last_hidden_state.max(dim=1)[0].squeeze().numpy()
            else:
                raise ValueError(f"Unknown pooling strategy: {pooling}")
            
            embeddings.append(embedding)
    
    embeddings = np.array(embeddings)
    logger.info(f"Embeddings shape: {embeddings.shape}")
    
    return embeddings


def demonstrate_semantic_similarity(
    texts: List[str],
    embeddings: np.ndarray
) -> None:
    """
    Demonstrate semantic similarity using cosine similarity.
    
    Args:
        texts: Input texts
        embeddings: BERT embeddings
    """
    logger.info("\n" + "=" * 80)
    logger.info("SEMANTIC SIMILARITY DEMO")
    logger.info("=" * 80)
    
    # Calculate pairwise cosine similarities
    similarities = cosine_similarity(embeddings)
    
    logger.info("\nPairwise Cosine Similarities:")
    logger.info("-" * 80)
    
    for i, text_i in enumerate(texts):
        logger.info(f"\n{i+1}. {text_i}")
        
        # Get most similar texts (excluding self)
        sim_scores = [(j, similarities[i, j]) for j in range(len(texts)) if j != i]
        sim_scores.sort(key=lambda x: x[1], reverse=True)
        
        logger.info("   Most similar:")
        for j, score in sim_scores[:3]:
            logger.info(f"     - {texts[j][:60]}... (similarity: {score:.4f})")


def semantic_search(
    query: str,
    corpus: List[str],
    tokenizer,
    model,
    top_k: int = 3
) -> List[Tuple[str, float]]:
    """
    Perform semantic search.
    
    Args:
        query: Search query
        corpus: List of documents to search
        tokenizer: BERT tokenizer
        model: BERT model
        top_k: Number of top results to return
        
    Returns:
        List of (document, similarity_score) tuples
    """
    logger.info("\n" + "=" * 80)
    logger.info("SEMANTIC SEARCH DEMO")
    logger.info("=" * 80)
    
    logger.info(f"\nQuery: {query}")
    
    # Get query embedding
    query_embedding = get_bert_embeddings([query], tokenizer, model)
    
    # Get corpus embeddings
    corpus_embeddings = get_bert_embeddings(corpus, tokenizer, model)
    
    # Calculate similarities
    similarities = cosine_similarity(query_embedding, corpus_embeddings)[0]
    
    # Get top-k results
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    results = [(corpus[i], similarities[i]) for i in top_indices]
    
    logger.info(f"\nTop {top_k} results:")
    for i, (doc, score) in enumerate(results, 1):
        logger.info(f"  {i}. {doc[:80]}... (score: {score:.4f})")
    
    return results


def visualize_embeddings(
    texts: List[str],
    embeddings: np.ndarray,
    save_path: str = None
) -> None:
    """
    Visualize embeddings using t-SNE.
    
    Args:
        texts: Input texts
        embeddings: BERT embeddings
        save_path: Optional path to save figure
    """
    logger.info("\n" + "=" * 80)
    logger.info("EMBEDDING VISUALIZATION (t-SNE)")
    logger.info("=" * 80)
    
    # Apply t-SNE
    logger.info("\nApplying t-SNE dimensionality reduction...")
    tsne = TSNE(n_components=2, random_state=42, perplexity=min(5, len(texts)-1))
    embeddings_2d = tsne.fit_transform(embeddings)
    
    # Plot
    plt.figure(figsize=(12, 8))
    plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], s=100, alpha=0.6)
    
    # Annotate points
    for i, text in enumerate(texts):
        label = text[:30] + "..." if len(text) > 30 else text
        plt.annotate(
            label,
            (embeddings_2d[i, 0], embeddings_2d[i, 1]),
            fontsize=8,
            alpha=0.7
        )
    
    plt.title('BERT Embeddings Visualization (t-SNE)', fontsize=14, fontweight='bold')
    plt.xlabel('t-SNE Component 1')
    plt.ylabel('t-SNE Component 2')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"\nVisualization saved to: {save_path}")
    
    plt.show()


def compare_embedding_methods() -> None:
    """
    Compare different embedding methods.
    """
    logger.info("\n" + "=" * 80)
    logger.info("EMBEDDING METHODS COMPARISON")
    logger.info("=" * 80)
    
    comparison = """
    | Method      | Dimension | Context-Aware | Pre-trained | Speed   |
    |-------------|-----------|---------------|-------------|---------|
    | BOW         | Vocab     | No            | No          | Fast    |
    | TF-IDF      | Vocab     | No            | No          | Fast    |
    | Word2Vec    | 100-300   | No            | Yes         | Fast    |
    | GloVe       | 50-300    | No            | Yes         | Fast    |
    | BERT        | 768-1024  | Yes           | Yes         | Slower  |
    
    Key Differences:
    - BOW/TF-IDF: Sparse, high-dimensional, no semantic meaning
    - Word2Vec/GloVe: Dense, fixed-size, captures word-level semantics
    - BERT: Dense, contextual (same word different meanings), state-of-the-art
    
    Use Cases:
    - BOW/TF-IDF: Fast baselines, interpretable features
    - Word2Vec/GloVe: Word similarity, analogies, fast inference
    - BERT: Semantic search, question answering, when accuracy matters
    """
    
    logger.info(comparison)


def main():
    """Main demonstration function."""
    logger.info("=" * 80)
    logger.info("DAY 3: BERT EMBEDDINGS AND SEMANTIC SIMILARITY")
    logger.info("=" * 80)
    
    # Load model
    tokenizer, model = load_bert_model("distilbert-base-uncased")
    
    # Sample texts
    texts = [
        "The cat sat on the mat.",
        "A feline rested on the rug.",
        "The dog played in the park.",
        "Machine learning is a subset of artificial intelligence.",
        "Deep learning uses neural networks.",
        "Natural language processing enables text understanding.",
        "Python is a popular programming language.",
        "Java is used for enterprise applications.",
    ]
    
    logger.info(f"\nProcessing {len(texts)} example texts")
    
    # Get embeddings
    embeddings = get_bert_embeddings(texts, tokenizer, model, pooling="mean")
    
    # Demonstrate semantic similarity
    demonstrate_semantic_similarity(texts, embeddings)
    
    # Semantic search
    corpus = [
        "Python is great for data science and machine learning.",
        "JavaScript is essential for web development.",
        "SQL is used for database management.",
        "R is popular for statistical analysis.",
        "Java is widely used in enterprise software.",
        "C++ is preferred for system programming.",
    ]
    
    query = "What language should I use for AI projects?"
    semantic_search(query, corpus, tokenizer, model, top_k=3)
    
    # Visualize embeddings
    output_dir = Path(__file__).parent.parent / "examples" / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    visualize_embeddings(
        texts,
        embeddings,
        save_path=str(output_dir / "embeddings_tsne.png")
    )
    
    # Compare methods
    compare_embedding_methods()
    
    logger.info("\n" + "=" * 80)
    logger.info("DEMO COMPLETE")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
