#!/bin/bash

# Copy input SCAN to output structure
mkdir -p data/output/en/scan
cp data/input/scan/tasks.txt data/output/en/scan/tasks.txt

# Translate SCAN
python ./src/preprocess_scan.py data/input/scan/tasks.txt data/output/fr/scan/tasks.txt fr
python ./src/preprocess_scan.py data/input/scan/tasks.txt data/output/ru/scan/tasks.txt ru
python ./src/preprocess_scan.py data/input/scan/tasks.txt data/output/hin/scan/tasks.txt hin
python ./src/preprocess_scan.py data/input/scan/tasks.txt data/output/cmn/scan/tasks.txt cmn

# Generate MCD splits
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
