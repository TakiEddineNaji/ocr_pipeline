# =====================================================
# STEP 2 — OCR USING PADDLEOCR (CALLABLE)
# =====================================================
# Purpose:
# - Run OCR on processed PNG images from Step 1
# - Preserve page order
# - Save raw OCR results in JSON
# =====================================================

import json
import re
from pathlib import Path
from paddleocr import PaddleOCR
import os

# -------------------------------
# OCR pipeline function
# -------------------------------
def run_ocr(input_dir, output_dir):
    """
    Run PaddleOCR on all PNG images in input_dir.

    Args:
        input_dir (str or Path): Folder containing processed_*.png images
        output_dir (str or Path): Folder to save OCR output JSON

    Returns:
        list: OCR results per image
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)  # Use the folder exactly as given
    output_json = output_path / "cv_ocr_raw.json"

    # Ensure output folder exists
    output_path.mkdir(parents=True, exist_ok=True)

    # Delete old JSON if exists
    if output_json.exists():
        os.remove(output_json)

    # Initialize OCR
    ocr = PaddleOCR(lang="fr", use_textline_orientation=False)

    # Numeric sort helper
    def numeric_key(path):
        m = re.search(r"(\d+)", path.name)
        return int(m.group(1)) if m else 0

    # Collect images
    image_paths = sorted(input_path.glob("processed_*.png"), key=numeric_key)
    if not image_paths:
        raise RuntimeError(f"No processed_*.png images found in {input_dir}")

    results = []

    for img_path in image_paths:
        print(f"OCR → {img_path.name}")
        ocr_result = ocr.ocr(str(img_path))
        lines = []

        for page in ocr_result:
            # VL container / new format
            if isinstance(page, dict) and "rec_texts" in page:
                rec_texts = page.get("rec_texts", [])
                rec_scores = page.get("rec_scores", [None] * len(rec_texts))
                for text, conf in zip(rec_texts, rec_scores):
                    lines.append({
                        "text": str(text),
                        "confidence": float(conf) if conf is not None else None,
                        "bbox": None
                    })
            # Legacy / hybrid format
            elif isinstance(page, (list, tuple)):
                for line in page:
                    if isinstance(line, (list, tuple)) and len(line) == 2:
                        bbox = line[0]
                        text, confidence = line[1]
                        lines.append({
                            "text": str(text),
                            "confidence": float(confidence),
                            "bbox": bbox
                        })
            else:
                continue

        results.append({
            "image": img_path.name,
            "lines": lines
        })

    # Save OCR output JSON
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"[STEP 2] OCR output saved → {output_json}")
    return results


# -------------------------------
# Optional CLI entry point
# -------------------------------
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python step2_ocr_paddle.py <input_dir> <output_dir>")
        sys.exit(1)

    run_ocr(sys.argv[1], sys.argv[2])
