#!/bin/bash
set -e

python src/rescore.py data/output/results/en/mcd1/results.json data/output/results/en/mcd1/score.json
# python src/rescore.py data/output/results/en/mcd2/results.json data/output/results/en/mcd2/score.json
# python src/rescore.py data/output/results/en/mcd3/results.json data/output/results/en/mcd3/score.json
python src/rescore.py data/output/results/en/add_prim_jump/results.json data/output/results/en/add_prim_jump/score.json
python src/rescore.py data/output/results/en/length_split/results.json data/output/results/en/length_split/score.json
python src/rescore.py data/output/results/en/simple/results.json data/output/results/en/simple/score.json

# python src/rescore.py data/output/results/en/add_prim_turn_left/results.json data/output/results/en/add_prim_turn_left/score.json
# python src/rescore.py data/output/results/en/length_split/results.json data/output/results/en/length_split/score.json
python src/rescore.py data/output/results/fr/mcd1/results.json data/output/results/fr/mcd1/score.json
# python src/rescore.py data/output/results/fr/mcd2/results.json data/output/results/fr/mcd2/score.json
# python src/rescore.py data/output/results/fr/mcd3/results.json data/output/results/fr/mcd3/score.json
python src/rescore.py data/output/results/fr/add_prim_jump/results.json data/output/results/fr/add_prim_jump/score.json
python src/rescore.py data/output/results/fr/length_split/results.json data/output/results/fr/length_split/score.json
python src/rescore.py data/output/results/fr/simple/results.json data/output/results/fr/simple/score.json

# python src/rescore.py data/output/results/fr/add_prim_turn_left/results.json data/output/results/fr/add_prim_turn_left/score.json
# python src/rescore.py data/output/results/fr/length_split/results.json data/output/results/fr/length_split/score.json
python src/rescore.py data/output/results/hin/mcd1/results.json data/output/results/hin/mcd1/score.json
# python src/rescore.py data/output/results/hin/mcd2/results.json data/output/results/hin/mcd2/score.json
# python src/rescore.py data/output/results/hin/mcd3/results.json data/output/results/hin/mcd3/score.json
python src/rescore.py data/output/results/hin/add_prim_jump/results.json data/output/results/hin/add_prim_jump/score.json
python src/rescore.py data/output/results/hin/length_split/results.json data/output/results/hin/length_split/score.json
python src/rescore.py data/output/results/hin/simple/results.json data/output/results/hin/simple/score.json

# python src/rescore.py data/output/results/hin/add_prim_turn_left/results.json data/output/results/hin/add_prim_turn_left/score.json
# python src/rescore.py data/output/results/hin/length_split/results.json data/output/results/hin/length_split/score.json
python src/rescore.py data/output/results/ru/mcd1/results.json data/output/results/ru/mcd1/score.json
# python src/rescore.py data/output/results/ru/mcd2/results.json data/output/results/ru/mcd2/score.json
# python src/rescore.py data/output/results/ru/mcd3/results.json data/output/results/ru/mcd3/score.json
python src/rescore.py data/output/results/ru/add_prim_jump/results.json data/output/results/ru/add_prim_jump/score.json 
python src/rescore.py data/output/results/ru/length_split/results.json data/output/results/ru/length_split/score.json
python src/rescore.py data/output/results/ru/simple/results.json data/output/results/ru/simple/score.json

# python src/rescore.py data/output/results/ru/add_prim_turn_left/results.json data/output/results/ru/add_prim_turn_left/score.json
# python src/rescore.py data/output/results/ru/length_split/results.json data/output/results/ru/length_split/score.json
python src/rescore.py data/output/results/cmn/mcd1/results.json data/output/results/cmn/mcd1/score.json
# python src/rescore.py data/output/results/cmn/mcd2/results.json data/output/results/cmn/mcd2/score.json
# python src/rescore.py data/output/results/cmn/mcd3/results.json data/output/results/cmn/mcd3/score.json
python src/rescore.py data/output/results/cmn/add_prim_jump/results.json data/output/results/cmn/add_prim_jump/score.json
python src/rescore.py data/output/results/cmn/length_split/results.json data/output/results/cmn/length_split/score.json
python src/rescore.py data/output/results/cmn/simple/results.json data/output/results/cmn/simple/score.json

# python src/rescore.py data/output/results/cmn/add_prim_turn_left/results.json data/output/results/cmn/add_prim_turn_left/score.json
# python src/rescore.py data/output/results/cmn/length_split/results.json data/output/results/cmn/length_split/score.json
