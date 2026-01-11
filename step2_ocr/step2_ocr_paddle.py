# =====================================================
# STEP 2 — OCR USING PADDLEOCR (DOCKER + GPU)
# =====================================================
# Input : directory of PNG images
# Output: cv_ocr_raw.json
# =====================================================

import subprocess
from pathlib import Path


DOCKER_IMAGE = "paddlecloud/paddleocr:2.6-gpu-cuda11.2-cudnn8-latest"
OCR_LANG = "fr"


def run_ocr(input_dir: str, output_dir: str):
    """
    Entry point expected by caller_batch.py
    """

    input_dir = Path(input_dir).resolve()
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    print("[STEP 2] OCR via Docker (GPU ENABLED + MODEL CACHE)")
    print(f"  Language: {OCR_LANG}")
    print(f"  Input   : {input_dir}")
    print(f"  Output  : {output_dir}")
    print(f"  Cache   : {Path.home() / '.paddleocr'}")

    docker_python = f"""
import json
from pathlib import Path
from paddleocr import PaddleOCR

ocr = PaddleOCR(lang="{OCR_LANG}", use_gpu=True)

pages = []
image_dir = Path("/input")
images = sorted(image_dir.glob("*.png"))

for idx, img_path in enumerate(images):
    result = ocr.ocr(str(img_path), cls=True)

    blocks = []
    if result and result[0]:
        for line in result[0]:
            blocks.append({{
                "text": line[1][0],
                "confidence": float(line[1][1]),
                "bbox": line[0]
            }})

    pages.append({{
        "page": idx + 1,
        "blocks": blocks
    }})

with open("/output/cv_ocr_raw.json", "w", encoding="utf-8") as f:
    json.dump({{"pages": pages}}, f, ensure_ascii=False, indent=2)
"""

    cmd = [
        "docker", "run", "--rm",
        "--gpus", "all",
        "-e", "FLAGS_use_gpu=1",
        "-v", f"{input_dir}:/input",
        "-v", f"{output_dir}:/output",
        "-v", f"{Path.home() / '.paddleocr'}:/root/.paddleocr",
        DOCKER_IMAGE,
        "python3", "-c", docker_python
    ]

    subprocess.run(cmd, check=True)

    output_file = output_dir / "cv_ocr_raw.json"
    if not output_file.exists():
        raise RuntimeError("Step 2 failed: cv_ocr_raw.json not created")

    print(f"[STEP 2] OCR completed → {output_dir}")
    return output_dir



# Optional CLI usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python step2_ocr_paddle.py <input_dir> <output_dir>")
        sys.exit(1)

    run_ocr(sys.argv[1], sys.argv[2])
