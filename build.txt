#!/bin/bash
set -e
echo "Installing dependencies..."
pip install -r requirements.txt
echo "Downloading model.zip..."
curl -L "https://drive.google.com/uc?export=download&id=12xlo1cEpPI8V6muAzc_uFWBk7hgfK3g6" -o model.zip
echo "Checking file type..."
file model.zip
echo "Extracting model.zip..."
unzip model.zip || { echo "Unzip failed! Check if model.zip is a valid ZIP file."; exit 1; }