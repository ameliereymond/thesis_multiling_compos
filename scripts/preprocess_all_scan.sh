#!/bin/bash

# # Copy input SCAN to output structure
mkdir -p data/output/en/scan
cp data/input/scan/tasks.txt data/output/en/scan/tasks.txt

# # Translate SCAN
python ./src/preprocess_scan.py data/input/scan/tasks.txt data/output/fr/scan/tasks.txt fr
python ./src/preprocess_scan.py data/input/scan/tasks.txt data/output/ru/scan/tasks.txt ru
python ./src/preprocess_scan.py data/input/scan/tasks.txt data/output/hin/scan/tasks.txt hin
python ./src/preprocess_scan.py data/input/scan/tasks.txt data/output/cmn/scan/tasks.txt cmn

# # Generate MCD splits
python ./src/split.py data/output/en/scan/tasks.txt data/output/en/mcd1 data/splits/mcd1.json
python ./src/split.py data/output/fr/scan/tasks.txt data/output/fr/mcd1 data/splits/mcd1.json
python ./src/split.py data/output/ru/scan/tasks.txt data/output/ru/mcd1 data/splits/mcd1.json
python ./src/split.py data/output/hin/scan/tasks.txt data/output/hin/mcd1 data/splits/mcd1.json
python ./src/split.py data/output/cmn/scan/tasks.txt data/output/cmn/mcd1 data/splits/mcd1.json

python ./src/split.py data/output/en/scan/tasks.txt data/output/en/mcd2 data/splits/mcd2.json
python ./src/split.py data/output/fr/scan/tasks.txt data/output/fr/mcd2 data/splits/mcd2.json
python ./src/split.py data/output/ru/scan/tasks.txt data/output/ru/mcd2 data/splits/mcd2.json
python ./src/split.py data/output/hin/scan/tasks.txt data/output/hin/mcd2 data/splits/mcd2.json
python ./src/split.py data/output/cmn/scan/tasks.txt data/output/cmn/mcd2 data/splits/mcd2.json

python ./src/split.py data/output/en/scan/tasks.txt data/output/en/mcd3 data/splits/mcd3.json
python ./src/split.py data/output/fr/scan/tasks.txt data/output/fr/mcd3 data/splits/mcd3.json
python ./src/split.py data/output/ru/scan/tasks.txt data/output/ru/mcd3 data/splits/mcd3.json
python ./src/split.py data/output/hin/scan/tasks.txt data/output/hin/mcd3 data/splits/mcd3.json
python ./src/split.py data/output/cmn/scan/tasks.txt data/output/cmn/mcd3 data/splits/mcd3.json

# # Generate add prim jump splits
python ./src/split.py data/output/en/scan/tasks.txt data/output/en/add_prim_jump data/output/splits/scan/add_prim_jump.json
python ./src/split.py data/output/fr/scan/tasks.txt data/output/fr/add_prim_jump data/output/splits/scan/add_prim_jump.json
python ./src/split.py data/output/ru/scan/tasks.txt data/output/ru/add_prim_jump data/output/splits/scan/add_prim_jump.json
python ./src/split.py data/output/hin/scan/tasks.txt data/output/hin/add_prim_jump data/output/splits/scan/add_prim_jump.json
python ./src/split.py data/output/cmn/scan/tasks.txt data/output/cmn/add_prim_jump data/output/splits/scan/add_prim_jump.json

# # Generate add prim turn left splits
python ./src/split.py data/output/en/scan/tasks.txt data/output/en/add_prim_turn_left data/output/splits/scan/add_prim_turn_left.json
python ./src/split.py data/output/fr/scan/tasks.txt data/output/fr/add_prim_turn_left data/output/splits/scan/add_prim_turn_left.json
python ./src/split.py data/output/ru/scan/tasks.txt data/output/ru/add_prim_turn_left data/output/splits/scan/add_prim_turn_left.json
python ./src/split.py data/output/hin/scan/tasks.txt data/output/hin/add_prim_turn_left data/output/splits/scan/add_prim_turn_left.json
python ./src/split.py data/output/cmn/scan/tasks.txt data/output/cmn/add_prim_turn_left data/output/splits/scan/add_prim_turn_left.json

# # Generate length splits
python ./src/split.py data/output/en/scan/tasks.txt data/output/en/length_split data/output/splits/scan/length_split.json
python ./src/split.py data/output/fr/scan/tasks.txt data/output/fr/length_split data/output/splits/scan/length_split.json
python ./src/split.py data/output/ru/scan/tasks.txt data/output/ru/length_split data/output/splits/scan/length_split.json
python ./src/split.py data/output/hin/scan/tasks.txt data/output/hin/length_split data/output/splits/scan/length_split.json
python ./src/split.py data/output/cmn/scan/tasks.txt data/output/cmn/length_split data/output/splits/scan/length_split.json

# Generate simple splits
python ./src/split.py data/output/en/scan/tasks.txt data/output/en/simple data/output/splits/scan/simple.json
python ./src/split.py data/output/fr/scan/tasks.txt data/output/fr/simple data/output/splits/scan/simple.json
python ./src/split.py data/output/ru/scan/tasks.txt data/output/ru/simple data/output/splits/scan/simple.json
python ./src/split.py data/output/hin/scan/tasks.txt data/output/hin/simple data/output/splits/scan/simple.json
python ./src/split.py data/output/cmn/scan/tasks.txt data/output/cmn/simple data/output/splits/scan/simple.json
