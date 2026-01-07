# =====================================================
# STEP 7 — LLM ANSWERING (RAG + OLLAMA)
# =====================================================
# Purpose:
# - Receive a user question
# - Retrieve relevant context from Chroma (Step 6)
# - Build a grounded prompt
# - Call local Ollama LLM (Qwen 2.5)
# - Return answer
# =====================================================

from step6_retrieval.step6_retrieval import main as retrieve_blocks
import ollama

# -----------------------------------------------------
# LLM CONFIG
# -----------------------------------------------------
MODEL_NAME = "qwen2.5:7b-instruct"


def build_prompt(context_blocks, question):
    context_text = "\n\n".join(context_blocks)

    prompt = f"""
You are an assistant answering questions ONLY using the provided context.
If the answer is not present in the context, say exactly:
"Not found in the CV".

CONTEXT:
{context_text}

QUESTION:
{question}

ANSWER:
"""
    return prompt.strip()


def call_llm(prompt):
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response["message"]["content"]


def answer_question(chroma_dir, question, top_k=3):
    # -------------------------------
    # Step 6 — Retrieval
    # -------------------------------
    results = retrieve_blocks(chroma_dir, question, top_k)

    context_blocks = results["documents"][0]

    if not context_blocks:
        return "Not found in the CV"

    # -------------------------------
    # Build prompt
    # -------------------------------
    prompt = build_prompt(context_blocks, question)

    # -------------------------------
    # Step 7 — LLM
    # -------------------------------
    answer = call_llm(prompt)

    return answer


# -----------------------------------------------------
# CLI
# -----------------------------------------------------
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python step7_llm_answering.py <chroma_dir> <question> [top_k]")
        sys.exit(1)

    answer = answer_question(
        chroma_dir=sys.argv[1],
        question=sys.argv[2],
        top_k=int(sys.argv[3]) if len(sys.argv) > 3 else 3
    )

    print("\n[STEP 7] Answer:\n")
    print(answer)
