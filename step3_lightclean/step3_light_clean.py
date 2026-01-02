# =====================================================
# STEP 3 — LIGHT OCR CLEANING (CALLABLE + CLI)
# =====================================================
# Purpose:
# - Remove low-confidence noise (optional)
# - Normalize spacing and accents
# - Preserve layout order if bbox exists
# - Keep all lines even if bbox is missing
# - Save cleaned JSON for downstream LLM/RAG
# =====================================================

import json
from pathlib import Path
from unidecode import unidecode


# -------------------------------
# Line-level cleaning
# -------------------------------
def clean_line(line, min_conf=0.30):
    """
    Clean a single OCR line.

    Rules:
    - Drop lines below min_conf (optional)
    - Normalize whitespace
    - Normalize accents
    - Keep lines even if bbox is None
    """
    confidence = line.get("confidence")
    if confidence is not None and confidence < min_conf:
        return None

    text = line.get("text", "")
    text = " ".join(text.split())
    if not text:
        return None

    return {
        "text": unidecode(text),
        "confidence": confidence,
        "bbox": line.get("bbox")  # can be None
    }


# -------------------------------
# Main cleaning function
# -------------------------------
def clean_ocr_json(input_path, output_path, min_conf=0.30, sort_by_bbox=True):
    """
    Clean OCR JSON from Step 2.

    Args:
        input_path (str | Path): raw OCR JSON
        output_path (str | Path): cleaned JSON path
        min_conf (float): confidence threshold
        sort_by_bbox (bool): sort lines by top-left coordinate if bbox exists

    Returns:
        list: cleaned OCR pages
    """
    input_path = Path(input_path)
    output_path = Path(output_path)

    if not input_path.exists():
        raise FileNotFoundError(f"OCR input file not found: {input_path}")

    with open(input_path, "r", encoding="utf-8") as f:
        pages = json.load(f)

    cleaned_pages = []

    for page in pages:
        cleaned_lines = []

        for line in page.get("lines", []):
            cl = clean_line(line, min_conf=min_conf)
            if cl:
                cleaned_lines.append(cl)

        # Optional: sort by bbox top-left if available
        if sort_by_bbox:
            cleaned_lines.sort(key=lambda l: (l["bbox"][0][1], l["bbox"][0][0]) if l["bbox"] else (0, 0))

        cleaned_pages.append({
            "image": page.get("image", ""),
            "lines": cleaned_lines
        })

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_pages, f, ensure_ascii=False, indent=2)

    print(f"[STEP 3] Cleaned OCR saved → {output_path}")
    return cleaned_pages


# -------------------------------
# CLI entry point
# -------------------------------
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python step3_light_clean_full.py <raw_ocr.json> <cleaned.json>")
        sys.exit(1)

    clean_ocr_json(
        input_path=sys.argv[1],
        output_path=sys.argv[2],
    )
