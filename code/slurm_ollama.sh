#!/bin/bash
#SBATCH --job-name=atlas-ollama
#SBATCH --partition=a100          # ADJUST: run  sinfo -o "%P %G %l" | grep -i gpu  and put your GPU partition here
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=120G
#SBATCH --time=24:00:00           # ADJUST to your partition's max; resubmit this job until the run completes
#SBATCH --output=atlas_ollama_%j.log

set -e
MODEL="qwen2.5:72b-instruct"      # use qwen2.5:32b-instruct on a 40GB GPU
SCRATCHDIR=${SCRATCH:-$HOME/scratch}

# user-space ollama install (first run only; skipped if present)
if [ ! -x "$HOME/ollama/bin/ollama" ]; then
  mkdir -p $HOME/ollama
  curl -L https://ollama.com/download/ollama-linux-amd64.tgz | tar -xz -C $HOME/ollama
fi
export PATH=$HOME/ollama/bin:$PATH
mkdir -p $SCRATCHDIR/ollama_models
export OLLAMA_MODELS=$SCRATCHDIR/ollama_models

ollama serve > $HOME/ollama_server_$SLURM_JOB_ID.log 2>&1 &
OLLAMA_PID=$!
until curl -sf http://localhost:11434/api/tags > /dev/null; do sleep 5; done
echo "ollama ready"
ollama pull $MODEL

cd $HOME/LLM_contamination     # first run:  git clone https://github.com/lyuhongju1/LLM_contamination  from the login node
nvidia-smi | head -15

# Amendment 5: target N=50; A and D first (the load-bearing contrast), then B and C.
# Every invocation is resumable; resubmit this job until the census prints.
python3 code/run_probe_local.py --model $MODEL --n 50 --num-ctx 32768 --conditions A D
python3 code/run_probe_local.py --model $MODEL --n 50 --num-ctx 32768 --conditions B C

kill $OLLAMA_PID
echo "COMPLETE"
