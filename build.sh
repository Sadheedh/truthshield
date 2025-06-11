#!/bin/bash
set -e
echo "Installing dependencies..."
pip install -r requirements.txt
echo "Downloading model.zip..."
curl -L "https://dl.dropbox.com/scl/fi/zljldm6e4v94lwtlhinv9/truthshield-api.zip?rlkey=i4rekent2i9ud2bey2mfp69qs&st=s21o4ej0&dl=1" -o model.zip
echo "Checking file type..."
file model.zip
echo "Extracting model.zip..."
unzip model.zip || { echo "Unzip failed! Check if model.zip is a valid ZIP file."; exit 1; }
