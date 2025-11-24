# NLP/NLU 3-Day Syllabus Project

![Project Logo](/mnt/data/ccc22d39-2631-4a6d-bf58-53e4e346dfd0.png)

[![CI](https://github.com/yourusername/nlp-nlu-3day/workflows/CI/badge.svg)](https://github.com/yourusername/nlp-nlu-3day/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A complete, reproducible VS Code project implementing a comprehensive 3-day NLP/NLU syllabus with runnable code, notebooks, tests, and CI/CD infrastructure.

## 📋 Overview

This project provides production-ready implementations of:

**Day 1: Tokenization, NER & Rule-Based Matching (spaCy)**
- Tokenization and sentence segmentation
- Lemmatization and POS tagging
- Named Entity Recognition (NER)
- Rule-based pattern matching

**Day 2: Feature Engineering & Classification**
- Bag of Words (BOW) and TF-IDF
- Sentiment classification (spaCy + sklearn)
- Topic classification (AG News)
- Model evaluation and comparison

**Day 3: Transformers & NLU**
- BERT embeddings and semantic similarity
- Fine-tuning transformers (HuggingFace)
- Abstractive summarization
- ROUGE and BLEU evaluation

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- 4GB RAM minimum (8GB recommended)
- ~2GB disk space for models and data

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/nlp-nlu-3day.git
cd nlp-nlu-3day

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy models
python -m spacy download en_core_web_sm

# (Optional) Download sample datasets
python data/download_data.py
```

### First Run

```bash
# Run smoke test to verify installation
python tests/test_smoke_model.py

# Run Day 1 tokenization demo
python nlp_day1/day1_tokenization_spacy.py

# Run Day 2 BOW/TF-IDF demo
python nlp_day2/bow_tfidf.py

# Run Day 3 embeddings demo
python nlu_day3/embeddings_experiments.py
```

## 📁 Project Structure

```
nlp-nlu-3day/
├── nlp_day1/                    # Day 1: Tokenization & NER
│   ├── day1_tokenization_spacy.py
│   ├── day1_ner_rulebased.py
│   └── notebook_day1.ipynb
├── nlp_day2/                    # Day 2: Feature Engineering
│   ├── bow_tfidf.py
│   ├── sentiment_spacy_project.py
│   ├── topic_classification.py
│   └── notebook_day2.ipynb
├── nlu_day3/                    # Day 3: Transformers & NLU
│   ├── embeddings_experiments.py
│   ├── hf_classification.py
│   ├── summarization_demo.py
│   ├── evaluation_metrics.py
│   └── notebook_day3.ipynb
├── data/                        # Data and samples
│   ├── download_data.py
│   └── samples/
│       ├── sentiment_small.csv
│       ├── topics_small.csv
│       ├── article.txt
│       └── ner_examples.txt
├── utils/                       # Shared utilities
│   ├── preprocessing.py
│   ├── metrics.py
│   └── config.yaml
├── tests/                       # Test suite
│   ├── test_preprocessing.py
│   ├── test_metrics.py
│   └── test_smoke_model.py
├── scripts/                     # Automation scripts
│   ├── run_all.sh
│   └── setup_spacy_models.sh
├── examples/outputs/            # Generated outputs
├── requirements.txt
├── Dockerfile
├── pyproject.toml
└── README.md
```

## 💻 Usage Examples

### Day 1: Tokenization and NER

```bash
# Tokenization, lemmatization, POS tagging
python nlp_day1/day1_tokenization_spacy.py

# Named Entity Recognition and rule-based matching
python nlp_day1/day1_ner_rulebased.py
```

**Expected runtime:** ~30 seconds each (CPU)

### Day 2: BOW, TF-IDF, Classification

```bash
# BOW and TF-IDF feature extraction
python nlp_day2/bow_tfidf.py --dataset data/samples/sentiment_small.csv

# Sentiment classification (spaCy + sklearn)
python nlp_day2/sentiment_spacy_project.py

# Topic classification (AG News)
python nlp_day2/topic_classification.py
```

**Expected runtime:** 1-2 minutes each (CPU)

### Day 3: Embeddings, Transformers, Summarization

```bash
# BERT embeddings and semantic similarity
python nlu_day3/embeddings_experiments.py

# Fine-tune transformer for classification (quick demo)
python nlu_day3/hf_classification.py --task sentiment --epochs 1 --subset 200

# Abstractive summarization with ROUGE/BLEU
python nlu_day3/summarization_demo.py --text_file data/samples/article.txt

# Evaluation metrics demonstration
python nlu_day3/evaluation_metrics.py
```

**Expected runtime:** 
- Embeddings: ~1 minute (CPU)
- HF classification: ~3 minutes (CPU, 1 epoch, 200 samples)
- Summarization: ~30 seconds (CPU)

### Run All Demos

```bash
# Execute all Day 1-3 scripts sequentially
bash scripts/run_all.sh
```

**Total runtime:** ~10 minutes (CPU)

## 📊 Jupyter Notebooks

Interactive notebooks with explanations and visualizations:

```bash
# Start Jupyter Lab
jupyter lab

# Open notebooks:
# - nlp_day1/notebook_day1.ipynb
# - nlp_day2/notebook_day2.ipynb
# - nlu_day3/notebook_day3.ipynb
```

## 🐳 Docker

### Build and Run

```bash
# Build Docker image
docker build -t nlp-nlu-3day .

# Run smoke test
docker run --rm nlp-nlu-3day

# Interactive shell
docker run -it --rm nlp-nlu-3day bash

# Run specific script
docker run --rm nlp-nlu-3day python nlp_day1/day1_tokenization_spacy.py
```

### GPU Support

```bash
# Run with GPU (requires nvidia-docker)
docker run --gpus all -it --rm nlp-nlu-3day
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=nlp_day1 --cov=nlp_day2 --cov=nlu_day3 --cov=utils

# Run smoke test only
python tests/test_smoke_model.py

# Linting
flake8 nlp_day1/ nlp_day2/ nlu_day3/ utils/ tests/
black --check nlp_day1/ nlp_day2/ nlu_day3/ utils/ tests/
```

## ⚙️ Configuration

All hyperparameters and paths are centralized in `utils/config.yaml`:

```yaml
random_seed: 42
models:
  bert_base: "distilbert-base-uncased"
  summarization: "sshleifer/distilbart-cnn-6-6"
training:
  batch_size: 16
  learning_rate: 2.0e-5
  num_epochs: 3
```

## 🔧 CPU vs GPU

### CPU Mode (Default)

All scripts run on CPU by default. Optimized for commodity hardware.

### GPU Mode

To enable GPU acceleration:

```python
# In your scripts, set device
import torch
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
```

Or set environment variable:

```bash
export CUDA_VISIBLE_DEVICES=0
```

## 📈 Expected Performance

### Model Accuracy (on sample datasets)

| Task | Model | Accuracy | F1 Score |
|------|-------|----------|----------|
| Sentiment | TF-IDF + LogReg | ~0.85 | ~0.84 |
| Sentiment | spaCy TextCat | ~0.80 | ~0.79 |
| Sentiment | DistilBERT | ~0.90 | ~0.90 |
| Topic | TF-IDF + SVM | ~0.88 | ~0.87 |

### Runtime Estimates (CPU, Intel i7)

| Script | Runtime | Notes |
|--------|---------|-------|
| Tokenization | 30s | spaCy processing |
| NER | 30s | Entity extraction |
| BOW/TF-IDF | 1m | Feature engineering |
| Sentiment (sklearn) | 2m | Training + eval |
| Topic Classification | 2m | Multi-class |
| BERT Embeddings | 1m | 8 sentences |
| HF Classification | 3m | 1 epoch, 200 samples |
| Summarization | 30s | Single article |

## 🎯 Learning Objectives

By working through this project, you will:

1. **Master spaCy** for tokenization, NER, and linguistic features
2. **Understand feature engineering** with BOW and TF-IDF
3. **Build ML classifiers** for sentiment and topic classification
4. **Work with transformers** using HuggingFace
5. **Extract BERT embeddings** for semantic tasks
6. **Fine-tune models** with the Trainer API
7. **Evaluate NLU systems** with ROUGE and BLEU
8. **Deploy with Docker** and CI/CD

## 🛠️ Development

### VS Code Dev Container

Open in VS Code with dev container support:

```bash
# Install Remote-Containers extension
# Open folder in container: Ctrl+Shift+P -> "Reopen in Container"
```

### Code Quality

```bash
# Format code
black nlp_day1/ nlp_day2/ nlu_day3/ utils/ tests/

# Lint
flake8 nlp_day1/ nlp_day2/ nlu_day3/ utils/ tests/

# Type checking (optional)
mypy nlp_day1/ nlp_day2/ nlu_day3/ utils/
```

## 📚 Resources

### Documentation

- [spaCy Documentation](https://spacy.io/usage)
- [HuggingFace Transformers](https://huggingface.co/docs/transformers)
- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)

### Datasets

- [IMDB Reviews](https://huggingface.co/datasets/imdb)
- [AG News](https://huggingface.co/datasets/ag_news)
- [CNN/DailyMail](https://huggingface.co/datasets/cnn_dailymail)

### Models

- [DistilBERT](https://huggingface.co/distilbert-base-uncased)
- [DistilBART](https://huggingface.co/sshleifer/distilbart-cnn-6-6)

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **spaCy** for industrial-strength NLP
- **HuggingFace** for democratizing transformers
- **scikit-learn** for machine learning fundamentals
- The open-source NLP community

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Made with ❤️ for NLP learners and practitioners**
