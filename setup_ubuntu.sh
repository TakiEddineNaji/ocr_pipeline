#!/bin/bash
set -e

echo "=== OCR Pipeline Ubuntu Setup (GPU) ==="

# -------------------------
# 0. System packages
# -------------------------
sudo apt update
sudo apt install -y \
  python3.10 \
  python3.10-venv \
  python3-pip \
  poppler-utils \
  libgl1 \
  libglib2.0-0 \
  curl \
  build-essential

# -------------------------
# 1. CUDA toolkit (needed for nvcc)
# -------------------------
sudo apt install -y nvidia-cuda-toolkit

# -------------------------
# 2. Ollama (LLM runtime)
# -------------------------
if ! command -v ollama &> /dev/null; then
  curl -fsSL https://ollama.com/install.sh | sh
fi

# -------------------------
# 3. Project venv
# -------------------------
if [ ! -d ".venv" ]; then
  python3.10 -m venv .venv
fi

source .venv/bin/activate

pip install --upgrade pip setuptools wheel
pip cache purge

# -------------------------
# 4. Install Python deps
# -------------------------
pip install -r requirements.txt

# -------------------------
# 5. Jupyter kernel
# -------------------------
python -m ipykernel install --user \
  --name ocr_pipeline \
  --display-name "OCR Pipeline (Python 3.10)"

echo "=== Setup complete ==="
echo "IMPORTANT:"
echo "- NVIDIA driver + cuDNN must be installed manually"
echo "- Activate venv before running:"
echo "  source .venv/bin/activate"
