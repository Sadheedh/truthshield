#!/bin/bash
set -e
echo "Installing dependencies..."
pip install -r requirements.txt
echo "Downloading model.zip..."
curl -L "https://dl.dropbox.com/scl/fi/fv4figkjgpuskyu8tstui/model.zip?rlkey=3e65qrupet9pufaa93c7r0zj0&st=te7ikt8z&dl=1" -o model.zip
echo "Checking file type..."
file model.zip
echo "Extracting model.zip..."
unzip model.zip || { echo "Unzip failed! Check if model.zip is a valid ZIP file."; exit 1; }


# https://dl.dropbox.com/scl/fi/yu5mtqxs3qqwe244y51qo/model.zip?rlkey=tdo9jj3yhetkf93xa4hyr8iao&st=itag7p3c&dl=1
# below is old model which is named as model_old in dropbox
# https://dl.dropbox.com/scl/fi/yu5mtqxs3qqwe244y51qo/model.zip?rlkey=tdo9jj3yhetkf93xa4hyr8iao&st=itag7p3c&dl=1
# New one: https://dl.dropbox.com/scl/fi/fv4figkjgpuskyu8tstui/model.zip?rlkey=3e65qrupet9pufaa93c7r0zj0&st=te7ikt8z&dl=1
