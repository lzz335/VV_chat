#!/bin/bash
source $(conda info --base)/etc/profile.d/conda.sh
conda activate xx # xx is your environment name

python demo.py
