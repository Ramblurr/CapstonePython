#!/bin/bash

echo "Downloading dataset"
wget http://binaryelysium.com/nasdaq-data.tar.bz2

echo "Extracting dataset"
tar xjf nasdaq-data.tar.bz2

echo "Renaming.."
mv infochimps_dataset_4777_download_16185/NASDAQ/ .
rm -rf infochimps_dataset_4777_download_16185

echo "Done"
