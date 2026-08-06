#!/bin/bash
#SBATCH --job-name=atlas-ollama
#SBATCH --account=bgde-delta-gpu
#SBATCH --partition=gpuA100x4
#SBATCH --gpus-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=60G
#SBATCH --time=24:00:00           # ADJUST to your partition's max; resubmit this job until the run completes
#SBATCH --output=atlas_ollama_%j.log

set -e
MODEL="qwen2.5:32b-instruct"      # use qwen2.5:32b-instruct on a 40GB GPU
SCRATCHDIR=/scratch/bgde/$USER
# user-space ollama install (first run only; skipped if present)
export PATH=$HOME/ollama/bin:$PATH
mkdir -p $SCRATCHDIR/ollama_models
export OLLAMA_MODELS=$SCRATCHDIR/ollama_models

ollama serve > $HOME/ollama_server_$SLURM_JOB_ID.log 2>&1 &
OLLAMA_PID=$!
until curl -sf http://localhost:11434/api/tags > /dev/null; do sleep 5; done
echo "ollama ready"
cd $HOME/LLM_contamination     # first run:  git clone https://github.com/lyuhongju1/LLM_contamination  from the login node
nvidia-smi | head -15

# Amendment 5: target N=50; A and D first (the load-bearing contrast), then B and C.
# Every invocation is resumable; resubmit this job until the census prints.
python3 code/run_probe_local.py --model $MODEL --n 50 --num-ctx 49152 --conditions A D
python3 code/run_probe_local.py --model $MODEL --n 50 --num-ctx 49152 --conditions B C

kill $OLLAMA_PID
echo "COMPLETE"
