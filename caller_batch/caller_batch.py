from pathlib import Path
import sys

# =====================================================
# PROJECT ROOT
# =====================================================

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

RAG_OUT = ROOT / "caller_batch" / "step4_rag_batch_output"

# =====================================================
# CONFIG
# =====================================================
CV_INPUT_DIR = ROOT / "caller_batch" / "cvs_input"

BASE_STEP1_OUT = ROOT / "caller_batch" / "step1_batch_output"
BASE_STEP2_OUT = ROOT / "caller_batch" / "step2_batch_output"
BASE_STEP3_OUT = ROOT / "caller_batch" / "step3_batch_output"
BASE_STEP4_OUT = ROOT / "caller_batch" / "step4_batch_output"
BASE_STEP5_OUT = ROOT / "caller_batch" / "step5_batch_output"


# =====================================================
# IMPORTS (package-based)
# =====================================================
from step1_preprocess.step1_preprocess_pdf import main as preprocess_file
from step2_ocr.step2_ocr_paddle import run_ocr
from step3_lightclean.step3_light_clean import clean_ocr_json
from step4_rag.step4_rag_prepare import main as prepare_rag_blocks
from step5_embeddings.step5_embeddings import main as build_embeddings

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
    step5_out = BASE_STEP5_OUT

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

    step3_out.mkdir(parents=True, exist_ok=True)

    raw_json = step2_out / "cv_ocr_raw.json"
    clean_json = step3_out / "cv_ocr_clean.json"

    if not raw_json.exists():
        print("[SKIP] No OCR output")
        continue

    try:
        clean_ocr_json(raw_json, clean_json)
    except Exception as e:
        print(f"[ERROR] Step 3 failed: {e}")
        continue



    # -------------------------------
    # Step 4 — Prepare RAG blocks
    # -------------------------------
    step4_out.mkdir(parents=True, exist_ok=True)

    rag_blocks = step4_out / "rag_blocks.json"


    try:
        prepare_rag_blocks(
            input_path=clean_json,
            output_path=rag_blocks,
            doc_id=cv_name
        )
    except Exception as e:
        print(f"[ERROR] Step 4 failed: {e}")
        continue


    # -------------------------------
    # Step 5 — Embeddings (GPU)
    # -------------------------------
    build_embeddings(
        blocks_path=rag_blocks,
        chroma_dir=step5_out
    )

