from pathlib import Path

# =====================================================
# Project root
# =====================================================
ROOT = Path(__file__).resolve().parent

# =====================================================
# STEP 1 — Preprocess PDF → images
# =====================================================
from step1_preprocess.step1_preprocess_pdf import main as preprocess_pdf

preprocess_pdf(
    file_path=ROOT / "step1_preprocess" / "cv.pdf",
    output_dir=ROOT / "step1_preprocess" / "step1_output",
    poppler_path=None  # Ubuntu: Poppler resolved via PATH
)

# =====================================================
# STEP 2 — OCR (GPU)
# =====================================================
from step2_ocr.step2_ocr_paddle import run_ocr

run_ocr(
    input_dir=ROOT / "step1_preprocess" / "step1_output",
    output_dir=ROOT / "step2_ocr" / "step2_output"
)

# =====================================================
# STEP 3 — Light OCR cleaning
# =====================================================
from step3_lightclean.step3_light_clean import clean_ocr_json

clean_ocr_json(
    input_path=ROOT / "step2_ocr" / "step2_output" / "cv_ocr_raw.json",
    output_path=ROOT / "step3_lightclean" / "step3_output" / "cv_ocr_cleaned.json"
)

# =====================================================
# STEP 4 — RAG preparation
# =====================================================
from step4_rag.step4_rag_prepare import main as prepare_rag_blocks

prepare_rag_blocks(
    input_path=ROOT / "step3_lightclean" / "step3_output" / "cv_ocr_cleaned.json",
    output_path=ROOT / "step4_rag" / "step4_output" / "cv_rag_blocks.json",
    doc_id="cv_001"
)

# =====================================================
# STEP 5 — Embeddings (GPU forced)
# =====================================================
from step5_embeddings.step5_embeddings import main as build_embeddings

build_embeddings(
    blocks_path=ROOT / "step4_rag" / "step4_output" / "cv_rag_blocks.json",
    chroma_dir=ROOT / "step5_embeddings" / "step5_output"
)

# =====================================================
# STEP 7 — LLM Answering (Step 6 used internally)
# =====================================================
from step7_llm.step7_llm_answering import answer_question

answer = answer_question(
    chroma_dir=ROOT / "step5_embeddings" / "step5_output",
    question="What experience does the candidate have in data science?",
    top_k=3
)

print("\n================ FINAL ANSWER ================\n")
print(answer)
