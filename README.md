# Readme

## Dependencies

When you are installing this for the first time, run:

```bash
conda env create --file environment.yml
```

After that, and on every new session, run:

```bash
conda activate mscan2
```

During development, add dependencies that you care about to `environment.yml`. Then run:

```bash
conda env update --file environment.yml --prune
```

## Usage

### Inference on HuggingFace Inference API

Set an environment variable with your Hugging Face token:

```bash
export HF_TOKEN="hf_..."
```

Then, to run an experiment, you can run:

```bash
python src/inference.py --model-name "bigscience/bloom" --train data/output/en/simple/train.txt --test data/output/en/simple/test.txt --output data/output/results/playground/results.json --context-size 2 --num-queries 1
```

### Inference on OpenAI inference API

Set an environment variable with your HuggingFace token:

```bash
export OPENAI_API_KEY="sk-..."
```

### Condor

Edit `condor-run.sh` with whatever you want to do in the Condor task, then run:

```bash
condor_submit condor-task.cmd
```

To see the queue, and see whether your job is running:

```bash
condor_q 
```
