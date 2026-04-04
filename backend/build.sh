#!/usr/bin/env bash
# Render Build Script — runs during deploy
set -e

echo "=== Installing dependencies ==="
pip install -r requirements.txt

echo "=== Generating training data ==="
python generate_training_data.py

echo "=== Training classifier ==="
python train_classifier.py

echo "=== Build complete ==="
