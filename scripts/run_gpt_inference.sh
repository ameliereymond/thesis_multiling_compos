#!/bin/bash
set -e

model="gpt-3.5-turbo"

# ENGLISH

python ./src/experiment_openai.py \
    --model-name $model \
    --train data/output/en/mcd1/train.txt \
    --test data/output/en/mcd1/test.txt \
    --output data/output/results/$model/en/mcd1/results.json

# python ./src/experiment_openai.py \
#     --model-name $model \
#     --train data/output/en/mcd2/train.txt \
#     --test data/output/en/mcd2/test.txt \
#     --output data/output/results/$model/en/mcd2/results.json

# python ./src/experiment_openai.py \
#     --model-name $model \
#     --train data/output/en/mcd3/train.txt \
#     --test data/output/en/mcd3/test.txt \
#     --output data/output/results/$model/en/mcd3/results.json

# python ./src/experiment_openai.py \
#     --model-name $model \
#     --train data/output/en/add_prim_jump/train.txt \
#     --test data/output/en/add_prim_jump/test.txt \
#     --output data/output/results/$model/en/add_prim_jump/results.json \
#     --special-handling add_prim_jump

# python ./src/experiment_openai.py \
#     --model-name $model \
#     --train data/output/en/add_prim_turn_left/train.txt \
#     --test data/output/en/add_prim_turn_left/test.txt \
#     --output data/output/results/$model/en/add_prim_turn_left/results.json \
#     --special-handling add_prim_turn_left

python ./src/experiment_openai.py \
    --model-name $model \
    --train data/output/en/length_split/train.txt \
    --test data/output/en/length_split/test.txt \
    --output data/output/results/$model/en/length_split/results.json

python ./src/experiment_openai.py \
    --model-name $model \
    --train data/output/en/simple/train.txt \
    --test data/output/en/simple/test.txt \
    --output data/output/results/$model/en/simple/results.json

# # FRENCH

# python ./src/experiment_openai.py \
#     --model-name $model \
#     --train data/output/fr/mcd1/train.txt \
#     --test data/output/fr/mcd1/test.txt \
#     --output data/output/results/$model/fr/mcd1/results.json

# # python ./src/experiment_openai.py \
# #     --model-name $model \
# #     --train data/output/fr/mcd2/train.txt \
# #     --test data/output/fr/mcd2/test.txt \
# #     --output data/output/results/$model/fr/mcd2/results.json

# # python ./src/experiment_openai.py \
# #     --model-name $model \
# #     --train data/output/fr/mcd3/train.txt \
# #     --test data/output/fr/mcd3/test.txt \
# #     --output data/output/results/$model/fr/mcd3/results.json

# # python ./src/experiment_openai.py \
# #     --model-name $model \
# #     --train data/output/fr/add_prim_jump/train.txt \
# #     --test data/output/fr/add_prim_jump/test.txt \
# #     --output data/output/results/$model/fr/add_prim_jump/results.json \
# #     --special-handling add_prim_jump

# # python ./src/experiment_openai.py \
# #     --model-name $model \
# #     --train data/output/fr/add_prim_turn_left/train.txt \
# #     --test data/output/fr/add_prim_turn_left/test.txt \
# #     --output data/output/results/$model/fr/add_prim_turn_left/results.json \
# #     --special-handling add_prim_turn_left

# python ./src/experiment_openai.py \
#     --model-name $model \
#     --train data/output/fr/length_split/train.txt \
#     --test data/output/fr/length_split/test.txt \
#     --output data/output/results/$model/fr/length_split/results.json

# python ./src/experiment_openai.py \
#     --model-name $model \
#     --train data/output/fr/simple/train.txt \
#     --test data/output/fr/simple/test.txt \
#     --output data/output/results/$model/fr/simple/results.json

# # HINDI

# python ./src/experiment_openai.py \
#     --model-name $model \
#     --train data/output/hin/mcd1/train.txt \
#     --test data/output/hin/mcd1/test.txt \
#     --output data/output/results/$model/hin/mcd1/results.json

# # python ./src/experiment_openai.py \
# #     --model-name $model \
# #     --train data/output/hin/mcd2/train.txt \
# #     --test data/output/hin/mcd2/test.txt \
# #     --output data/output/results/$model/hin/mcd2/results.json

# # python ./src/experiment_openai.py \
# #     --model-name $model \
# #     --train data/output/hin/mcd3/train.txt \
# #     --test data/output/hin/mcd3/test.txt \
# #     --output data/output/results/$model/hin/mcd3/results.json

# # python ./src/experiment_openai.py \
# #     --model-name $model \
# #     --train data/output/hin/add_prim_jump/train.txt \
# #     --test data/output/hin/add_prim_jump/test.txt \
# #     --output data/output/results/$model/hin/add_prim_jump/results.json \
# #     --special-handling add_prim_jump

# # python ./src/experiment_openai.py \
# #     --model-name $model \
# #     --train data/output/hin/add_prim_turn_left/train.txt \
# #     --test data/output/hin/add_prim_turn_left/test.txt \
# #     --output data/output/results/$model/hin/add_prim_turn_left/results.json \
# #     --special-handling add_prim_turn_left

# python ./src/experiment_openai.py \
#     --model-name $model \
#     --train data/output/hin/length_split/train.txt \
#     --test data/output/hin/length_split/test.txt \
#     --output data/output/results/$model/hin/length_split/results.json

# python ./src/experiment_openai.py \
#     --model-name $model \
#     --train data/output/hin/simple/train.txt \
#     --test data/output/hin/simple/test.txt \
#     --output data/output/results/$model/hin/simple/results.json


# # RUSSIAN

# python ./src/experiment_openai.py \
#     --model-name $model \
#     --train data/output/ru/mcd1/train.txt \
#     --test data/output/ru/mcd1/test.txt \
#     --output data/output/results/$model/ru/mcd1/results.json

# # python ./src/experiment_openai.py \
# #     --model-name $model \
# #     --train data/output/ru/mcd2/train.txt \
# #     --test data/output/ru/mcd2/test.txt \
# #     --output data/output/results/$model/ru/mcd2/results.json

# # python ./src/experiment_openai.py \
# #     --model-name $model \
# #     --train data/output/ru/mcd3/train.txt \
# #     --test data/output/ru/mcd3/test.txt \
# #     --output data/output/results/$model/ru/mcd3/results.json

# # python ./src/experiment_openai.py \
# #     --model-name $model \
# #     --train data/output/ru/add_prim_jump/train.txt \
# #     --test data/output/ru/add_prim_jump/test.txt \
# #     --output data/output/results/$model/ru/add_prim_jump/results.json \
# #     --special-handling add_prim_jump

# # python ./src/experiment_openai.py \
# #     --model-name $model \
# #     --train data/output/ru/add_prim_turn_left/train.txt \
# #     --test data/output/ru/add_prim_turn_left/test.txt \
# #     --output data/output/results/$model/ru/add_prim_turn_left/results.json \
# #     --special-handling add_prim_turn_left

# python ./src/experiment_openai.py \
#     --model-name $model \
#    --train data/output/ru/length_split/train.txt \
#    --test data/output/ru/length_split/test.txt \
#    --output data/output/results/$model/ru/length_split/results.json

# python ./src/experiment_openai.py \
#     --model-name $model \
#    --train data/output/ru/simple/train.txt \
#    --test data/output/ru/simple/test.txt \
#    --output data/output/results/$model/ru/simple/results.json 

# # CHINESE MANDARIN

# python ./src/experiment_openai.py \
#     --model-name $model \
#     --train data/output/cmn/mcd1/train.txt \
#     --test data/output/cmn/mcd1/test.txt \
#     --output data/output/results/$model/cmn/mcd1/results.json

# # python ./src/experiment_openai.py \
# #     --model-name $model \
# #     --train data/output/cmn/mcd2/train.txt \
# #     --test data/output/cmn/mcd2/test.txt \
# #     --output data/output/results/$model/cmn/mcd2/results.json

# # python ./src/experiment_openai.py \
# #     --model-name $model \
# #     --train data/output/cmn/mcd3/train.txt \
# #     --test data/output/cmn/mcd3/test.txt \
# #     --output data/output/results/$model/cmn/mcd3/results.json

# # python ./src/experiment_openai.py \
# #     --model-name $model \
# #     --train data/output/cmn/add_prim_jump/train.txt \
# #     --test data/output/cmn/add_prim_jump/test.txt \
# #     --output data/output/results/$model/cmn/add_prim_jump/results.json \
# #     --special-handling add_prim_jump

# # python ./src/experiment_openai.py \
# #     --model-name $model \
# #     --train data/output/cmn/add_prim_turn_left/train.txt \
# #     --test data/output/cmn/add_prim_turn_left/test.txt \
# #     --output data/output/results/$model/cmn/add_prim_turn_left/results.json \
# #     --special-handling add_prim_turn_left

# python ./src/experiment_openai.py \
#     --model-name $model \
#    --train data/output/cmn/length_split/train.txt \
#    --test data/output/cmn/length_split/test.txt \
#    --output data/output/results/$model/cmn/length_split/results.json

# python ./src/experiment_openai.py \
#     --model-name $model \
#    --train data/output/cmn/simple/train.txt \
#    --test data/output/cmn/simple/test.txt \
#    --output data/output/results/$model/cmn/simple/results.json
