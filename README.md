# Readme

## Usage

To use the inference scripts, you must first set an environment variable with your Hugging Face token:

```
export HF_TOKEN="hf_..."
```

Then, to run an experiment, you can run:

```bash
python src/inference.py --model-name "bigscience/bloom" --train data/output/en/simple/train.txt --test data/output/en/simple/test.txt --output data/output/results/playground/results.json --context-size 2 --num-queries 1
```