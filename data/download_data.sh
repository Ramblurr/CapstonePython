#!/bin/bash

file="https://s3.amazonaws.com/infochimps/data/4777/16185/20100217033442/infochimps_dataset_4777_download_16185-csv.tar.bz2?AWSAccessKeyId=02S6Y1EFA7ZZ7KCZH3G2&Expires=1300847693&Signature=V7z6nfwkMsjmHYNiGmGoP014kcE%3D"

echo "Downloading dataset"
wget $file -O nasdaq-data.tar.bz2

echo "Extracting dataset"
tar xjf nasdaq-data.tar.bz2

echo "Renaming.."
mv infochimps_dataset_4777_download_16185/NASDAQ/ .
rm -rf infochimps_dataset_4777_download_16185

echo "Done"
