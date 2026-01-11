# =====================================================
# STEP 7 — LLM ANSWERING (RAG + OLLAMA)
# =====================================================
# Purpose:
# - Receive a user question
# - Retrieve aggregated candidate data from Step 6
# - Build one grounded prompt per candidate
# - Call local Ollama LLM (Qwen 2.5)
# - Return candidate-level answers
# =====================================================

from step6_retrieval.step6_retrieval import main as retrieve_blocks
import ollama

# -----------------------------------------------------
# LLM CONFIG
# -----------------------------------------------------
MODEL_NAME = "qwen2.5:7b-instruct"


# -----------------------------------------------------
# PROMPT BUILDER
# -----------------------------------------------------
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


# -----------------------------------------------------
# LLM CALL
# -----------------------------------------------------
def call_llm(prompt):
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response["message"]["content"]


# -----------------------------------------------------
# MAIN ENTRY POINT
# -----------------------------------------------------
def answer_question(chroma_dir, question, top_k=3):
    # -------------------------------
    # Step 6 — Retrieval (aggregated)
    # -------------------------------
    results = retrieve_blocks(chroma_dir, question, top_k)

    if not results:
        return "Not found in the CVs"

    answers = []

    # -------------------------------
    # Reason per candidate
    # -------------------------------
    for cv_id, blocks in results.items():
        context_blocks = [b["text"] for b in blocks]

        prompt = build_prompt(context_blocks, question)
        answer = call_llm(prompt)

        answers.append(
            f"Candidate {cv_id}:\n{answer}"
        )

    # -------------------------------
    # Final multi-candidate answer
    # -------------------------------
    return "\n\n".join(answers)


# -----------------------------------------------------
# CLI
# -----------------------------------------------------
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python step7_llm_answering.py <chroma_dir> <question> [top_k]")
        sys.exit(1)

    chroma_dir = sys.argv[1]
    question = sys.argv[2]
    top_k = int(sys.argv[3]) if len(sys.argv) > 3 else 3

    answer = answer_question(
        chroma_dir=chroma_dir,
        question=question,
        top_k=top_k
    )

    print("\n[STEP 7] Answer:\n")
    print(answer)
