#!/bin/bash
conda init bash
conda activate mscan2

export CUDA_VISIBLE_DEVICES="0,1"
python src/gpu_test.py > run-gpu.out

python ./src/experiment_xglm.py \
    --train data/output/en/simple/train.txt \
    --test data/output/en/simple/test.txt \
    --output data/output/results/xglm/en/simple/results.json \
    --num-queries 20 \
     > run-xglm-en-simple.out

python ./src/experiment_llama.py \
    --train data/output/en/simple/train.txt \
    --test data/output/en/simple/test.txt \
    --output data/output/results/llama/en/simple/results.json \
    --num-queries 20 \
     > run-llama-en-simple.out