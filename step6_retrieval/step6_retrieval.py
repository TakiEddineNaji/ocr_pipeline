# =====================================================
# STEP 6 — RETRIEVAL + AGGREGATION (CHROMA)
# =====================================================
# Purpose:
# - Retrieve relevant text blocks from Chroma
# - Group them by candidate (doc_id)
# - Provide candidate-level context for LLM reasoning
# =====================================================

import chromadb
from sentence_transformers import SentenceTransformer
from collections import defaultdict

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"


def main(chroma_dir, query, top_k=10):
    # -------------------------------
    # Load embedding model (GPU)
    # -------------------------------
    model = SentenceTransformer(EMBEDDING_MODEL_NAME, device="cuda")

    # -------------------------------
    # Connect to Chroma
    # -------------------------------
    client = chromadb.Client(
        settings=chromadb.Settings(
            persist_directory=str(chroma_dir),
            is_persistent=True,
            anonymized_telemetry=False
        )
    )

    collection = client.get_collection(name="cv_blocks")

    # -------------------------------
    # Encode query
    # -------------------------------
    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    )

    # -------------------------------
    # Vector search
    # -------------------------------
    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=top_k
    )

    # -------------------------------
    # AGGREGATION BY CANDIDATE (doc_id)
    # -------------------------------
    grouped = defaultdict(list)

    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        grouped[meta["doc_id"]].append({
            "page": meta["page"],
            "block_id": meta["block_id"],
            "text": doc
        })

    # -------------------------------
    # OUTPUT (candidate-level)
    # -------------------------------
    print("\n[STEP 6] Retrieved candidates:\n")

    for doc_id, blocks in grouped.items():
        print(f"Candidate: {doc_id}")
        for block in blocks:
            print(f"  Page {block['page']} | Block {block['block_id']}:")
            print(f"    {block['text'][:300]}")
        print()

    return grouped


# -------------------------------
# CLI
# -------------------------------
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python step6_retrieval.py <chroma_dir> <query> [top_k]")
        sys.exit(1)

    chroma_dir = sys.argv[1]
    query = sys.argv[2]
    top_k = int(sys.argv[3]) if len(sys.argv) > 3 else 10

    main(chroma_dir, query, top_k)
