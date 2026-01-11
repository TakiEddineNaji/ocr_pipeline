# =====================================================
# STEP 5 — EMBEDDINGS (CHROMA, IDEMPOTENT)
# =====================================================
# Purpose:
# - Embed RAG blocks into a persistent Chroma DB
# - Skip blocks that are already embedded
# - Allow incremental updates (safe re-runs)
# =====================================================

import json
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

# -------------------------------
# CONFIG
# -------------------------------
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# -------------------------------
# MAIN
# -------------------------------
def main(blocks_path, chroma_dir):
    blocks_path = Path(blocks_path)
    chroma_dir = Path(chroma_dir)

    if not blocks_path.exists():
        raise FileNotFoundError(f"Blocks file not found: {blocks_path}")

    # Load blocks
    with open(blocks_path, "r", encoding="utf-8") as f:
        blocks = json.load(f)

    if not blocks:
        print("[STEP 5] No blocks to embed")
        return

    # Load embedding model (GPU if available)
    model = SentenceTransformer(EMBEDDING_MODEL, device="cuda")

    # Connect to persistent Chroma DB
    client = chromadb.Client(
        settings=chromadb.Settings(
            persist_directory=str(chroma_dir),
            is_persistent=True,
            anonymized_telemetry=False
        )
    )

    collection = client.get_or_create_collection(name="cv_blocks")

    added = 0
    skipped = 0

    # -------------------------------
    # Embed blocks incrementally
    # -------------------------------
    for block in blocks:
        block_id = f"{block['doc_id']}_p{block['page']}_b{block['block_id']}"

        # Check if already embedded
        existing = collection.get(ids=[block_id])
        if existing["ids"]:
            skipped += 1
            continue

        # Embed text
        embedding = model.encode(
            block["text"],
            normalize_embeddings=True
        )

        # Store in Chroma
        collection.add(
            ids=[block_id],
            documents=[block["text"]],
            embeddings=[embedding.tolist()],
            metadatas=[{
                "doc_id": block["doc_id"],
                "page": block["page"],
                "block_id": block["block_id"]
            }]
        )

        added += 1

    print(f"[STEP 5] Added {added} new blocks")
    print(f"[STEP 5] Skipped {skipped} existing blocks")
    print(f"[STEP 5] Chroma DB directory: {chroma_dir.resolve()}")


# -------------------------------
# CLI
# -------------------------------
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python step5_embeddings.py <blocks.json> <chroma_dir>")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])
