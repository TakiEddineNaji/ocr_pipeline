OCR PIPELINE — UBUNTU SETUP
GPU • OCR • RAG • OLLAMA
============================================================

This document describes the complete setup required to run
the OCR pipeline on Ubuntu 22.04 with:
- NVIDIA GPU
- PaddleOCR (GPU)
- Persistent RAG (Chroma)
- Ollama LLM runtime


------------------------------------------------------------
1. SYSTEM PREREQUISITES (ONE TIME)
------------------------------------------------------------

sudo apt update
sudo apt install -y \
  python3.10 \
  python3.10-venv \
  python3-pip \
  poppler-utils \
  libgl1 \
  libglib2.0-0 \
  build-essential \
  curl


------------------------------------------------------------
2. NVIDIA GPU + DRIVER (MANUAL)
------------------------------------------------------------

Requirements:
- NVIDIA GPU
- NVIDIA driver installed
- nvidia-smi works

Notes:
- GPU drivers are system-level
- NOT installed via pip or virtualenv


------------------------------------------------------------
3. CUDA TOOLKIT (nvcc)
------------------------------------------------------------

sudo apt install -y nvidia-cuda-toolkit

Verify:
nvcc --version


------------------------------------------------------------
4. cuDNN (SYSTEM LEVEL)
------------------------------------------------------------

Install cuDNN 8.9.7 compatible with CUDA 11.x
(from NVIDIA website).

Optional verification:
ls /usr/lib/x86_64-linux-gnu | grep cudnn


------------------------------------------------------------
5. OLLAMA (LLM RUNTIME)
------------------------------------------------------------

Install Ollama:
curl -fsSL https://ollama.com/install.sh | sh

Pull model:
ollama pull qwen2.5:7b-instruct

Test model:
ollama run qwen2.5:7b-instruct

(Optional) Start daemon manually:
ollama serve


------------------------------------------------------------
6. GO TO PROJECT ROOT
------------------------------------------------------------

cd ~/Documents/github/ocr_pipeline


------------------------------------------------------------
7. PYTHON VIRTUAL ENV (NO SUDO)
------------------------------------------------------------

python3.10 -m venv .venv
source .venv/bin/activate

Verify:
which python

Expected:
.../ocr_pipeline/.venv/bin/python


------------------------------------------------------------
8. UPGRADE PIP (IMPORTANT)
------------------------------------------------------------

pip install --upgrade pip setuptools wheel
pip cache purge


------------------------------------------------------------
9. INSTALL PROJECT REQUIREMENTS
------------------------------------------------------------

pip install -r requirements.txt


------------------------------------------------------------
10. JUPYTER SUPPORT (OPTIONAL)
------------------------------------------------------------

pip install ipykernel

python -m ipykernel install --user \
  --name ocr_pipeline \
  --display-name "OCR Pipeline (Python 3.10)"


------------------------------------------------------------
11. SANITY CHECKS
------------------------------------------------------------

Paddle + CUDA:
python -c "import paddle; print(paddle.__version__, paddle.is_compiled_with_cuda())"

Expected output:
2.6.1 True

Ollama:
ollama list


------------------------------------------------------------
12. RUNNING THE PIPELINE
------------------------------------------------------------

Ingest documents (Steps 1–5, run once):
python calling_script.py
or
python caller_batch.py

Ask questions (Step 7, run anytime):
python step7_llm/step7_llm_answering.py \
  step5_embeddings/step5_output \
  "Quelle est l'expérience du candidat en data science ?"


------------------------------------------------------------
13. JUPYTER WORKFLOW
------------------------------------------------------------

from pathlib import Path
ROOT = Path.cwd()

Workflow:
- Step 1 → Step 5 : run once
- Step 6           : debug only
- Step 7           : run as many times as needed


------------------------------------------------------------
FINAL VALIDATED STACK
------------------------------------------------------------

OS            : Ubuntu 22.04
Python        : 3.10.x
CUDA          : 11.x
cuDNN         : 8.9.7
Paddle GPU    : 2.6.1
PaddleOCR     : 2.7.0
OpenCV        : 4.6.0
NumPy         : 1.26.x
Vector DB     : Chroma (disk-persistent)
LLM Runtime   : Ollama
LLM Model     : Qwen 2.5 (7B Instruct)


------------------------------------------------------------
IMPORTANT NOTES
------------------------------------------------------------

- NEVER commit .venv/
- NEVER commit chroma.sqlite3 or index/
- Embeddings are disk-persistent
- Restarting kernel or PC does NOT lose data
- Step 6 only works if Step 5 has been run successfully

============================================================
END OF FILE
============================================================
