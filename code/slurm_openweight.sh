#!/bin/bash
#SBATCH --job-name=atlas-openweight
#SBATCH --partition=a100          # ADJUST: your cluster's GPU partition name
#SBATCH --gres=gpu:2              # 2x80GB for Qwen2.5-72B bf16; use gpu:1 for 32B
#SBATCH --cpus-per-task=16
#SBATCH --mem=200G
#SBATCH --time=08:00:00
#SBATCH --output=atlas_openweight_%j.log

set -e
module purge
module load anaconda 2>/dev/null || module load python 2>/dev/null || true

# one-time env (comment out after first run):
# python -m venv $HOME/vllm-env
source $HOME/vllm-env/bin/activate
# pip install vllm   # one-time, ~10 min

MODEL="Qwen/Qwen2.5-72B-Instruct"
CTX=32768   # protodune auto-skipped at this context (documented subset)

python -m vllm.entrypoints.openai.api_server \
  --model $MODEL --tensor-parallel-size 2 \
  --max-model-len $CTX --port 8000 &
VLLM_PID=$!

# wait for the server to come up (model download ~140GB on first run)
until curl -sf http://localhost:8000/v1/models > /dev/null; do sleep 15; done
echo "vLLM ready"

cd $HOME/LLM_contamination    # git clone https://github.com/lyuhongju1/LLM_contamination first
export OPENWEIGHT_API_KEY=dummy
python code/run_probe_openweight.py \
  --base-url http://localhost:8000/v1 --model $MODEL \
  --n 20 --workers 8 --max-prompt-tokens $CTX

kill $VLLM_PID
