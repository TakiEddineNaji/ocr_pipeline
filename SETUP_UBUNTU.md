# OCR PIPELINE – UBUNTU SETUP (GPU + RAG + OLLAMA)

This document lists EVERYTHING required to run the OCR pipeline  
on Ubuntu 22.04 with NVIDIA GPU, PaddleOCR (GPU), RAG, ChromaDB, and Ollama.

==================================================
0) SYSTEM PREREQUISITES (ONE TIME)
==================================================

```bash
sudo apt update
sudo apt install -y \
  python3.10 \
  python3.10-venv \
  python3-pip \
  poppler-utils \
  libgl1 \
  libglib2.0-0 \
  build-essential \
  curl \
  git
```

==================================================
1) NVIDIA DRIVER + GPU (MANUAL)
==================================================

Required (must already work):

- NVIDIA driver installed
- `nvidia-smi` works
- CUDA **driver** compatible with CUDA 11.x or 12.x

⚠️ IMPORTANT:
- **Do NOT install CUDA via pip**
- **Do NOT rely on system CUDA toolkit version**
- Paddle uses **its own CUDA runtime**

You do **NOT** need `nvcc` for this project.

==================================================
2) CUDA TOOLKIT (OPTIONAL – NOT REQUIRED)
==================================================

⚠️ This step is **NOT required** for the OCR pipeline.

Only install if you explicitly need `nvcc`:

```bash
sudo apt install -y nvidia-cuda-toolkit
nvcc --version
```

Otherwise, **skip this step**.

==================================================
3) OLLAMA (LLM RUNTIME)
==================================================

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen2.5:7b-instruct
```

==================================================
4) GO TO PROJECT ROOT
==================================================

```bash
cd ~/Documents/github/ocr_pipeline
```

==================================================
5) PYTHON VIRTUAL ENV (NO SUDO)
==================================================

```bash
python3.10 -m venv .venv
source .venv/bin/activate
```

==================================================
6) INSTALL REQUIREMENTS
==================================================

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

==================================================
7) RUN PIPELINE
==================================================

```bash
python caller_batch.py
```

==================================================
8) ASK QUESTIONS
==================================================

```bash
python step7_llm/step7_llm_answering.py \
caller_batch/step5_batch_output \
"Quelle est l'expérience des candidats ?"
```

==================================================
FINAL NOTES
==================================================

- Do NOT upgrade NumPy to 2.x
- Do NOT upgrade Paddle without validation
- One shared Chroma DB is used for all CVs