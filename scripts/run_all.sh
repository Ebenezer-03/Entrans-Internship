#!/bin/bash

# Master script to run all NLP/NLU demos
# Executes Day 1, Day 2, and Day 3 scripts sequentially

set -e  # Exit on error

echo "=========================================="
echo "NLP/NLU 3-Day Project - Running All Demos"
echo "=========================================="

# Create output directories
mkdir -p examples/outputs
mkdir -p logs

# Redirect output to log file
LOG_FILE="logs/run_all_$(date +%Y%m%d_%H%M%S).log"
exec > >(tee -a "$LOG_FILE") 2>&1

echo ""
echo "Log file: $LOG_FILE"
echo ""

# Data preparation
echo "=========================================="
echo "Step 1: Preparing Data"
echo "=========================================="
python data/download_data.py

# Day 1: Tokenization and NER
echo ""
echo "=========================================="
echo "Step 2: Day 1 - Tokenization and NER"
echo "=========================================="

echo ""
echo "Running tokenization demo..."
python nlp_day1/day1_tokenization_spacy.py

echo ""
echo "Running NER demo..."
python nlp_day1/day1_ner_rulebased.py

# Day 2: BOW, TF-IDF, Classification
echo ""
echo "=========================================="
echo "Step 3: Day 2 - BOW, TF-IDF, Classification"
echo "=========================================="

echo ""
echo "Running BOW/TF-IDF demo..."
python nlp_day2/bow_tfidf.py

echo ""
echo "Running sentiment classification..."
python nlp_day2/sentiment_spacy_project.py

echo ""
echo "Running topic classification..."
python nlp_day2/topic_classification.py

# Day 3: Embeddings, Transformers, Summarization
echo ""
echo "=========================================="
echo "Step 4: Day 3 - Embeddings and Transformers"
echo "=========================================="

echo ""
echo "Running embeddings experiments..."
python nlu_day3/embeddings_experiments.py

echo ""
echo "Running evaluation metrics demo..."
python nlu_day3/evaluation_metrics.py

echo ""
echo "Running summarization demo..."
python nlu_day3/summarization_demo.py

# Optional: HuggingFace classification (slower)
read -p "Run HuggingFace classification (takes ~3 min)? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo ""
    echo "Running HuggingFace classification..."
    python nlu_day3/hf_classification.py --task sentiment --epochs 1 --subset 200
fi

# Summary
echo ""
echo "=========================================="
echo "All Demos Complete!"
echo "=========================================="
echo ""
echo "Outputs saved to: examples/outputs/"
echo "Log file: $LOG_FILE"
echo ""
echo "Next steps:"
echo "  - View generated visualizations in examples/outputs/"
echo "  - Check logs for detailed output"
echo "  - Run individual scripts for specific demos"
echo ""
