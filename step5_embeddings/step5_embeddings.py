# =====================================================
# STEP 5 — EMBEDDINGS (CHROMA)
# =====================================================

import json
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def main(blocks_path, chroma_dir):
    blocks_path = Path(blocks_path)
    chroma_dir = Path(chroma_dir)

    with open(blocks_path, "r", encoding="utf-8") as f:
        blocks = json.load(f)

    if not blocks:
        raise ValueError("No blocks found in input JSON")

    model = SentenceTransformer(EMBEDDING_MODEL, device="cuda")

    client = chromadb.Client(
    settings=chromadb.Settings(
        persist_directory=str(chroma_dir),
        is_persistent=True,      # 🔴 FORCE DISK
        anonymized_telemetry=False
    )
)


    collection = client.get_or_create_collection(
        name="cv_blocks"
    )

    texts = [b["text"] for b in blocks]
    embeddings = model.encode(
        texts,
        normalize_embeddings=True
    )

    ids = [f"block_{i}" for i in range(len(blocks))]
    metadatas = [
        {
            "doc_id": b["doc_id"],
            "page": b["page"],
            "block_id": b["block_id"]
        }
        for b in blocks
    ]

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )

    # ✅ AUTO-PERSIST (no client.persist() anymore)
    print(f"[STEP 5] Stored {len(blocks)} embeddings")
    print(f"[STEP 5] Chroma directory: {chroma_dir.resolve()}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python step5_embeddings.py <blocks.json> <chroma_dir>")
        exit(1)

    main(sys.argv[1], sys.argv[2])
