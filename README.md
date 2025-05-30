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

### Create split files

The SCAN repo gives us the pre-split data, while the MCD splits give a JSON description of how to split. The following script converts the SCAN splits to the same format as MCD.

```bash
./scripts/create_split_files.sh
```

### Preprocess

The following translates the English to various languages, then uses the split JSON descriptions to produces datasets for each (language, split) pair.

```bash
./scripts/preprocess_all_scan.sh
```

### Generate prompts

For each language and split, we can generate a bunch of few-shot prompts:

```bash
python src/generate_prompts.py
```

### Inference on HuggingFace Inference API

Set an environment variable with your Hugging Face token:

```bash
export HF_TOKEN="hf_..."
```

Or even better, create a `.env` file with your token (the code will pick it up):

```bash
HF_TOKEN="hf_..."
```

Then, to run an experiment, you can run:

```bash
python src/inference.py --model-name "bigscience/bloom" --train data/output/en/simple/train.txt --test data/output/en/simple/test.txt --output data/output/results/playground/results.json --context-size 2 --num-queries 1
```

### Inference on OpenAI inference API

Set an environment variable with your OpenAI token:

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

### SLURM

Start by generating all SLURM submission scripts

```bash
python src/generate_slurm.py
```

#### Run a single job

To run a single SLURM job, do e.g.:

```bash
sbatch scripts/generated/slurm/bloomz/run-bloomz-en-mcd1.slurm
```

Then check job status with:

```bash
squeue --me

# or, for more information:
squeue --me -o "%22S %.12i %.45j %.10T %.10M %.30R" --sort="M,j"
```

And check job output with e.g.:

```bash
# Replace job ID and task ID below
cat /mmfs1/gscratch/clmbr/amelie/projects/thesis_multiling_compos/data/output/results/bloomz/en/mcd1/<task_id>_<job_id>.out
```

#### Run all jobs

```bash
./scripts/generated/slurm/bloomz/slurm-submit-all.sh
```

### Aggregate scores

Once you've run all experiments, you can aggregate scores into a single CSV file for doing further analysis. Run:

```bash
python src/aggregate_scores.py
```

This will output a CSV file in `data/output/results/aggregated_scores.csv`.