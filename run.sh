#!/bin/bash
source $(conda info --base)/etc/profile.d/conda.sh
conda activate xx # xx is your environment name

DATABASE_PATH="Your path" # example: "C:/NeurIPS2025/open source/database"
URL_PATH="Your URL" # 你所使用的AI服务提供商的api
KEY="Your key" # example: "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
MODEL="gpt-4o-mini"


python demo.py --chroma_path "$DATABASE_PATH" --openai_base_url "$URL_PATH" --openai_api_key "$KEY" --model "$MODEL"