OCR PIPELINE – UBUNTU SETUP (GPU + RAG + OLLAMA)

This file lists EVERYTHING required to run the OCR pipeline
on Ubuntu 22.04 with NVIDIA GPU, PaddleOCR (GPU), RAG, and Ollama.

==================================================
0) SYSTEM PREREQUISITES (ONE TIME)
==================================================

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

==================================================
1) NVIDIA DRIVER + GPU (MANUAL)
==================================================

- NVIDIA driver installed
- nvidia-smi works
- CUDA 11.5
- cuDNN 8.9.7 (CUDA 11 compatible)

NOTE:
GPU drivers and cuDNN are SYSTEM-LEVEL.
They are NOT installed via pip or venv.

==================================================
2) CUDA TOOLKIT (nvcc)
==================================================

sudo apt install -y nvidia-cuda-toolkit

Verify:
nvcc --version

==================================================
3) OLLAMA (LLM RUNTIME)
==================================================

curl -fsSL https://ollama.com/install.sh | sh

Pull model:
ollama pull qwen2.5:7b-instruct

Test:
ollama run qwen2.5:7b-instruct

==================================================
4) GO TO PROJECT ROOT
==================================================

cd ~/Documents/github/ocr_pipeline

==================================================
5) PYTHON VIRTUAL ENV (NO SUDO)
==================================================

python3.10 -m venv .venv
source .venv/bin/activate

Verify:
which python
(must point to .venv/bin/python)

==================================================
6) UPGRADE PIP (IMPORTANT)
==================================================

pip install --upgrade pip setuptools wheel
pip cache purge

==================================================
7) INSTALL PROJECT REQUIREMENTS
==================================================

pip install -r requirements.txt

==================================================
8) JUPYTER SUPPORT (OPTIONAL BUT RECOMMENDED)
==================================================

pip install ipykernel
python -m ipykernel install --user \
  --name ocr_pipeline \
  --display-name "OCR Pipeline (Python 3.10)"

==================================================
9) SANITY CHECKS
==================================================

Python:
python -c "import paddle; print(paddle.__version__, paddle.is_compiled_with_cuda())"

Expected:
2.6.1 True

Ollama:
ollama list

==================================================
10) RUNNING THE PROJECT
==================================================

Ingest CVs (Steps 1–5, run once):
python calling_script.py
or
python caller_batch.py

Ask questions (Step 7, run anytime):
python step7_llm/step7_llm_answering.py step5_embeddings/step5_output \
"Quelle est l'expérience du candidat en data science ?"

==================================================
JUPYTER WORKFLOW
==================================================

from pathlib import Path
ROOT = Path.cwd()

Then:
- Step 1 → Step 5: run once
- Step 6: debug only
- Step 7: run as many times as needed

==================================================
FINAL VALIDATED STACK
==================================================

Python: 3.10.x
CUDA: 11.5
cuDNN: 8.9.7
Paddle GPU: 2.6.1
PaddleOCR: 2.7.0
OpenCV: 4.6.0
NumPy: 1.26.x
LLM: Qwen 2.5 (Ollama)

