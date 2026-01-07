from pathlib import Path

# =====================================================
# PROJECT ROOT
# =====================================================
ROOT = Path(__file__).resolve().parent

# =====================================================
# CONFIG
# =====================================================
CV_INPUT_DIR = ROOT / "caller_batch" / "cvs_input"

BASE_STEP1_OUT = ROOT / "caller_batch" / "step1_batch_output"
BASE_STEP2_OUT = ROOT / "caller_batch" / "step2_batch_output"
BASE_STEP3_OUT = ROOT / "caller_batch" / "step3_batch_output"
BASE_STEP4_OUT = ROOT / "caller_batch" / "step4_batch_output"
BASE_STEP5_OUT = ROOT / "caller_batch" / "step5_batch_output"

QUESTION = "What experience does the candidate have in data science?"
TOP_K = 3

# =====================================================
# IMPORTS (package-based)
# =====================================================
from step1_preprocess.step1_preprocess_pdf import main as preprocess_file
from step2_ocr.step2_ocr_paddle import run_ocr
from step3_lightclean.step3_light_clean import clean_ocr_json
from step4_rag.step4_rag_prepare import main as prepare_rag_blocks
from step5_embeddings.step5_embeddings import main as build_embeddings
from step7_llm.step7_llm_answering import answer_question

# =====================================================
# BATCH PIPELINE
# =====================================================
VALID_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}

for file_path in CV_INPUT_DIR.iterdir():
    if file_path.suffix.lower() not in VALID_EXTENSIONS:
        continue

    cv_name = file_path.stem
    print(f"\n=== Processing CV: {cv_name} ===")

    # Per-CV folders
    step1_out = BASE_STEP1_OUT / cv_name
    step2_out = BASE_STEP2_OUT / cv_name
    step3_out = BASE_STEP3_OUT / cv_name
    step4_out = BASE_STEP4_OUT / cv_name
    step5_out = BASE_STEP5_OUT / cv_name

    step5_out.mkdir(parents=True, exist_ok=True)

    # -------------------------------
    # Step 1 — Preprocess
    # -------------------------------
    preprocess_file(
        file_path=file_path,
        output_dir=step1_out,
        poppler_path=None  # Ubuntu
    )

    # -------------------------------
    # Step 2 — OCR (GPU)
    # -------------------------------
    try:
        run_ocr(step1_out, step2_out)
    except Exception as e:
        print(f"[ERROR] Step 2 failed: {e}")
        continue

    raw_json = step2_out / "cv_ocr_raw.json"
    if not raw_json.exists():
        print("[SKIP] No OCR output")
        continue

    # -------------------------------
    # Step 3 — Light clean
    # -------------------------------
    clean_json = step3_out / "cv_ocr_cleaned.json"
    step3_out.mkdir(parents=True, exist_ok=True)

    try:
        clean_ocr_json(raw_json, clean_json)
    except Exception as e:
        print(f"[ERROR] Step 3 failed: {e}")
        continue

    # -------------------------------
    # Step 4 — RAG blocks
    # -------------------------------
    rag_blocks = step4_out / "cv_rag_blocks.json"
    step4_out.mkdir(parents=True, exist_ok=True)

    prepare_rag_blocks(
        input_path=clean_json,
        output_path=rag_blocks,
        doc_id=cv_name
    )

    # -------------------------------
    # Step 5 — Embeddings (GPU)
    # -------------------------------
    build_embeddings(
        blocks_path=rag_blocks,
        chroma_dir=step5_out
    )

    # -------------------------------
    # Step 7 — LLM Answering
    # (Step 6 is used internally)
    # -------------------------------
    answer = answer_question(
        chroma_dir=step5_out,
        question=QUESTION,
        top_k=TOP_K
    )

    print("\n--- ANSWER ---")
    print(answer)
    print(f"[DONE] {cv_name}")
