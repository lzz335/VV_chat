#!/bin/bash
source $(conda info --base)/etc/profile.d/conda.sh
conda activate xx # xx is your environment name
FOLDER_PATH="vv"
DATABASE_PATH="Your path" #example: "C:/NeurIPS2025/open source/database"
BATCH_SIZE=8
URL_PATH="Your URL" # 你所使用的AI服务提供商的api
KEY="Your key" # example: "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
MODEL="gpt-4o-mini"

python train_database.py "$FOLDER_PATH" "$DATABASE_PATH" "$BATCH_SIZE"
