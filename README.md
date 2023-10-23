# Readme

## Installation

When you are installing this for the first time, run:

```bash
conda env create --file environment.yml
```

After that, and on every new session, run:

```bash
conda activate mscan2
```

## Usage

To use the inference scripts, you must first set an environment variable with your Hugging Face token:

```
export HF_TOKEN="hf_..."
```

Then, to run an experiment, you can run:

```bash
python src/inference.py --model-name "bigscience/bloom" --train data/output/en/simple/train.txt --test data/output/en/simple/test.txt --output data/output/results/playground/results.json --context-size 2 --num-queries 1
```

## Development
### Adding dependencies

Add dependencies that you care about to `environment.yml`