#!/bin/bash

# Setup script for spaCy models
# Downloads required spaCy models for the project

set -e  # Exit on error

echo "=================================="
echo "Setting up spaCy models..."
echo "=================================="

# Download small English model
echo ""
echo "Downloading en_core_web_sm..."
python -m spacy download en_core_web_sm

# Optional: Download transformer-based model (larger, slower, more accurate)
read -p "Download en_core_web_trf (transformer model, ~500MB)? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Downloading en_core_web_trf..."
    python -m spacy download en_core_web_trf
else
    echo "Skipping en_core_web_trf"
fi

echo ""
echo "=================================="
echo "spaCy models setup complete!"
echo "=================================="
