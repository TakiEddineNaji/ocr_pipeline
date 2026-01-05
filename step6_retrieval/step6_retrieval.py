# =====================================================
# STEP 6 — RETRIEVAL (CHROMA)
# =====================================================

import chromadb
from sentence_transformers import SentenceTransformer

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"


def main(chroma_dir, query, top_k=3):
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    client = chromadb.Client(
        settings=chromadb.Settings(
            persist_directory=chroma_dir,
            anonymized_telemetry=False
        )
    )

    collection = client.get_collection(name="cv_blocks")

    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    )

    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=top_k
    )

    print("\n[STEP 6] Retrieved blocks:\n")
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        print(f"Doc: {meta['doc_id']} | Page: {meta['page']}")
        print(doc[:300], "\n")

    return results


if __name__ == "__main__":
    import sys
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 3)
