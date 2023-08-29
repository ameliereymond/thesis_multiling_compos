#!/bin/bash

python src/verification.py data/output/en/scan/tasks.txt data/output/fr/scan/tasks.txt data/output/fr/scan/verif.txt
python src/verification.py data/output/en/scan/tasks.txt data/output/ru/scan/tasks.txt data/output/ru/scan/verif.txt
python src/verification.py data/output/en/scan/tasks.txt data/output/cmn/scan/tasks.txt data/output/cmn/scan/verif.txt
python src/verification.py data/output/en/scan/tasks.txt data/output/hin/scan/tasks.txt data/output/hin/scan/verif.txt