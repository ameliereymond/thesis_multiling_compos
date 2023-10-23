#!/bin/bash
conda init bash
conda activate mscan

./scripts/run_xglm_inference.sh > run.out
