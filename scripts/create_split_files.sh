#!/bin/bash

python ./src/create_split_file.py \
    --source data/input/scan/tasks.txt \
    --train data/input/scan/length_split/tasks_train_length.txt \
    --test data/input/scan/length_split/tasks_test_length.txt \
    --output data/output/splits/scan/length_split.json

python ./src/create_split_file.py \
    --source data/input/scan/tasks.txt \
    --train  data/input/scan/add_prim_split/tasks_train_addprim_jump.txt \
    --test data/input/scan/add_prim_split/tasks_test_addprim_jump.txt \
    --output data/output/splits/scan/add_prim_jump.json

python ./src/create_split_file.py \
    --source data/input/scan/tasks.txt \
    --train  data/input/scan/add_prim_split/tasks_train_addprim_turn_left.txt \
    --test data/input/scan/add_prim_split/tasks_test_addprim_turn_left.txt \
    --output data/output/splits/scan/add_prim_turn_left.json
