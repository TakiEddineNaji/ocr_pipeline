# =====================================================
# STEP 3 — LIGHT OCR CLEANING (CALLABLE)
# =====================================================
# Purpose:
# - Remove low-confidence noise
# - Normalize spacing and accents
# - Preserve layout order
# - NO semantic interpretation
# =====================================================

import json
from unidecode import unidecode
from pathlib import Path
import os

# -------------------------------
# Line-level cleaning
# -------------------------------
def clean_line(line, min_conf=0.30):
    """
    Clean a single OCR line:
    - Remove low-confidence lines
    - Normalize spaces and accents
    - Skip empty text or missing bbox
    """
    if line["confidence"] is None or line["confidence"] < min_conf:
        return None

    text = " ".join(line["text"].split())
    if not text:
        return None

    if not line.get("bbox"):
        return None

    return {
        "text": unidecode(text),
        "bbox": line["bbox"]
    }


# -------------------------------
# Main cleaning function
# -------------------------------
def clean_ocr_json(input_path, output_path, min_conf=0.30):
    """
    Clean OCR JSON from Step 2:
    - input_path: path to raw OCR JSON
    - output_path: path to save cleaned JSON
    - min_conf: minimum confidence threshold
    """
    input_path = Path(input_path)
    output_path = Path(output_path)

    # Read raw OCR
    with open(input_path, "r", encoding="utf-8") as f:
        pages = json.load(f)

    cleaned_pages = []

    for page in pages:
        cleaned_lines = []

        for line in page.get("lines", []):
            cl = clean_line(line, min_conf=min_conf)
            if cl:
                cleaned_lines.append(cl)

        # Sort by top-left coordinate (y, then x)
        cleaned_lines.sort(key=lambda l: (l["bbox"][0][1], l["bbox"][0][0]))

        cleaned_pages.append({
            "image": page.get("image", ""),
            "lines": cleaned_lines
        })

    # Ensure output folder exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save cleaned JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_pages, f, ensure_ascii=False, indent=2)

    print(f"[STEP 3] Cleaned OCR saved → {output_path}")
    return cleaned_pages


# -------------------------------
# Optional CLI entry point
# -------------------------------
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python step3_light_clean_callable.py <raw_ocr.json> <cleaned.json>")
        sys.exit(1)

    clean_ocr_json(sys.argv[1], sys.argv[2])
