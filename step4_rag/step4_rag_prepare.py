# =====================================================
# STEP 4 — RAG PREPARATION (CV-SAFE BLOCK BUILDING)
# =====================================================
# Purpose:
# - Convert cleaned OCR lines into dense, meaningful blocks
# - Optimize for embeddings and retrieval
# - Absorb CV layout fragmentation
# - Preserve page boundaries and traceability
# =====================================================

import json
from pathlib import Path


MAX_WORDS_PER_BLOCK = 120   # sweet spot for CVs


def normalize_text(text: str) -> str:
    """
    Light normalization only (NO semantics).
    """
    return " ".join(text.split())


def build_blocks(cleaned_pages, doc_id):
    blocks = []
    block_id = 0

    for page_idx, page in enumerate(cleaned_pages, start=1):
        current_words = []

        for line in page.get("lines", []):
            text = line.get("text", "").strip()
            if not text:
                continue

            text = normalize_text(text)
            current_words.extend(text.split())

            # Flush if block is large enough
            if len(current_words) >= MAX_WORDS_PER_BLOCK:
                blocks.append({
                    "doc_id": doc_id,
                    "page": page_idx,
                    "block_id": block_id,
                    "text": " ".join(current_words)
                })
                block_id += 1
                current_words = []

        # Flush remainder at end of page
        if current_words:
            blocks.append({
                "doc_id": doc_id,
                "page": page_idx,
                "block_id": block_id,
                "text": " ".join(current_words)
            })
            block_id += 1

    return blocks


def main(input_path, output_path, doc_id):
    input_path = Path(input_path)
    output_path = Path(output_path)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    with open(input_path, "r", encoding="utf-8") as f:
        cleaned_pages = json.load(f)

    rag_blocks = build_blocks(cleaned_pages, doc_id)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(rag_blocks, f, ensure_ascii=False, indent=2)

    print(f"[STEP 4] RAG blocks saved → {output_path}")
    print(f"[STEP 4] Total blocks: {len(rag_blocks)}")

    return rag_blocks


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 4:
        print("Usage: python step4_rag_prepare.py <cleaned.json> <rag_blocks.json> <doc_id>")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2], sys.argv[3])
