#!/bin/bash
set -e

# ENGLISH

# python ./src/bloom_inference.py \
#    --train data/output/en/mcd1/train.txt \
#    --test data/output/en/mcd1/test.txt \
#    --output data/output/results/en/mcd1/results.json

# python ./src/bloom_inference.py \
#    --train data/output/en/mcd2/train.txt \
#    --test data/output/en/mcd2/test.txt \
#    --output data/output/results/en/mcd2/results.json

# python ./src/bloom_inference.py \
#    --train data/output/en/mcd3/train.txt \
#    --test data/output/en/mcd3/test.txt \
#    --output data/output/results/en/mcd3/results.json

# python ./src/bloom_inference.py \
#    --train data/output/en/add_prim_jump/train.txt \
#    --test data/output/en/add_prim_jump/test.txt \
#    --output data/output/results/en/add_prim_jump/results.json

# python ./src/bloom_inference.py \
#    --train data/output/en/add_prim_turn_left/train.txt \
#    --test data/output/en/add_prim_turn_left/test.txt \
#    --output data/output/results/en/add_prim_turn_left/results.json

# python ./src/bloom_inference.py \
#    --train data/output/en/length_split/train.txt \
#    --test data/output/en/length_split/test.txt \
#    --output data/output/results/en/length_split/results.json

# FRENCH

# python ./src/bloom_inference.py \
#    --train data/output/fr/mcd1/train.txt \
#    --test data/output/fr/mcd1/test.txt \
#    --output data/output/results/fr/mcd1/results.json

# python ./src/bloom_inference.py \
#    --train data/output/fr/mcd2/train.txt \
#    --test data/output/fr/mcd2/test.txt \
#    --output data/output/results/fr/mcd2/results.json

# python ./src/bloom_inference.py \
#    --train data/output/fr/mcd3/train.txt \
#    --test data/output/fr/mcd3/test.txt \
#    --output data/output/results/fr/mcd3/results.json

# python ./src/bloom_inference.py \
#    --train data/output/fr/add_prim_jump/train.txt \
#    --test data/output/fr/add_prim_jump/test.txt \
#    --output data/output/results/fr/add_prim_jump/results.json

# python ./src/bloom_inference.py \
#    --train data/output/fr/add_prim_turn_left/train.txt \
#    --test data/output/fr/add_prim_turn_left/test.txt \
#    --output data/output/results/fr/add_prim_turn_left/results.json

# python ./src/bloom_inference.py \
#    --train data/output/fr/length_split/train.txt \
#    --test data/output/fr/length_split/test.txt \
#    --output data/output/results/fr/length_split/results.json

# HINDI

# python ./src/bloom_inference.py \
#    --train data/output/hin/mcd1/train.txt \
#    --test data/output/hin/mcd1/test.txt \
#    --output data/output/results/hin/mcd1/results.json

# python ./src/bloom_inference.py \
#    --train data/output/hin/mcd2/train.txt \
#    --test data/output/hin/mcd2/test.txt \
#    --output data/output/results/hin/mcd2/results.json

# python ./src/bloom_inference.py \
#    --train data/output/hin/mcd3/train.txt \
#    --test data/output/hin/mcd3/test.txt \
#    --output data/output/results/hin/mcd3/results.json

# python ./src/bloom_inference.py \
#    --train data/output/hin/add_prim_jump/train.txt \
#    --test data/output/hin/add_prim_jump/test.txt \
#    --output data/output/results/hin/add_prim_jump/results.json

# python ./src/bloom_inference.py \
#    --train data/output/hin/add_prim_turn_left/train.txt \
#    --test data/output/hin/add_prim_turn_left/test.txt \
#    --output data/output/results/hin/add_prim_turn_left/results.json

# python ./src/bloom_inference.py \
#    --train data/output/hin/length_split/train.txt \
#    --test data/output/hin/length_split/test.txt \
#    --output data/output/results/hin/length_split/results.json

# RUSSIAN

# python ./src/bloom_inference.py \
#     --train data/output/ru/mcd1/train.txt \
#     --test data/output/ru/mcd1/test.txt \
#     --output data/output/results/ru/mcd1/results.json \
#     --context-size 8

# python ./src/bloom_inference.py \
#    --train data/output/ru/mcd2/train.txt \
#    --test data/output/ru/mcd2/test.txt \
#    --output data/output/results/ru/mcd2/results.json

# python ./src/bloom_inference.py \
#    --train data/output/ru/mcd3/train.txt \
#    --test data/output/ru/mcd3/test.txt \
#    --output data/output/results/ru/mcd3/results.json

python ./src/bloom_inference.py \
    --train data/output/ru/add_prim_jump/train.txt \
    --test data/output/ru/add_prim_jump/test.txt \
    --output data/output/results/ru/add_prim_jump/results.json \
    --context-size 8

# python ./src/bloom_inference.py \
#    --train data/output/ru/add_prim_turn_left/train.txt \
#    --test data/output/ru/add_prim_turn_left/test.txt \
#    --output data/output/results/ru/add_prim_turn_left/results.json

# python ./src/bloom_inference.py \
#    --train data/output/ru/length_split/train.txt \
#    --test data/output/ru/length_split/test.txt \
#    --output data/output/results/ru/length_split/results.json

# CHINESE MANDARIN

python ./src/bloom_inference.py \
    --train data/output/cmn/mcd1/train.txt \
    --test data/output/cmn/mcd1/test.txt \
    --output data/output/results/cmn/mcd1/results.json

# python ./src/bloom_inference.py \
#    --train data/output/cmn/mcd2/train.txt \
#    --test data/output/cmn/mcd2/test.txt \
#    --output data/output/results/cmn/mcd2/results.json

# python ./src/bloom_inference.py \
#    --train data/output/cmn/mcd3/train.txt \
#    --test data/output/cmn/mcd3/test.txt \
#    --output data/output/results/cmn/mcd3/results.json

python ./src/bloom_inference.py \
    --train data/output/cmn/add_prim_jump/train.txt \
    --test data/output/cmn/add_prim_jump/test.txt \
    --output data/output/results/cmn/add_prim_jump/results.json

# python ./src/bloom_inference.py \
#    --train data/output/cmn/add_prim_turn_left/train.txt \
#    --test data/output/cmn/add_prim_turn_left/test.txt \
#    --output data/output/results/cmn/add_prim_turn_left/results.json

# python ./src/bloom_inference.py \
#    --train data/output/cmn/length_split/train.txt \
#    --test data/output/cmn/length_split/test.txt \
#    --output data/output/results/cmn/length_split/results.json
