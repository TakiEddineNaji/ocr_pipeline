# =====================================================
# STEP 3 — LIGHT CLEAN OCR JSON (STRUCTURE PRESERVING)
# =====================================================

import json
from pathlib import Path


def clean_ocr_json(input_json: Path, output_json: Path):
    with open(input_json, "r", encoding="utf-8") as f:
        raw = json.load(f)

    raw_pages = raw.get("pages", [])
    cleaned_pages = []

    for page in raw_pages:
        lines = []

        for block in page.get("blocks", []):
            text = block.get("text", "").strip()
            if not text:
                continue

            lines.append({
                "text": text,
                "confidence": block.get("confidence"),
                "bbox": block.get("bbox")
            })

        cleaned_pages.append({
            "page_num": page.get("page"),
            "lines": lines
        })

    output_json.parent.mkdir(parents=True, exist_ok=True)
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(cleaned_pages, f, ensure_ascii=False, indent=2)

    print(f"[STEP 3] Cleaned OCR saved → {output_json}")

