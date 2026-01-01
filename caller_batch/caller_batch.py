import sys
from pathlib import Path

# =====================================================
# CONFIG
# =====================================================
CV_INPUT_DIR = Path(r"C:\ocr-pipeline\cvs_input")

BASE_STEP1_OUT = Path(r"C:\ocr-pipeline\step1_preprocess\batch_output")
BASE_STEP2_OUT = Path(r"C:\ocr-pipeline\step2_ocr\batch_output")
BASE_STEP3_OUT = Path(r"C:\ocr-pipeline\step3_lightclean\batch_output")

POPPLER_PATH = r"C:\poppler\Library\bin"

# =====================================================
# STEP 1 IMPORT
# =====================================================
step1_folder = r"C:\ocr-pipeline\step1_preprocess"
sys.path.append(step1_folder)
from step1_preprocess_pdf import main as preprocess_pdf

# =====================================================
# STEP 2 IMPORT
# =====================================================
step2_folder = r"C:\ocr-pipeline\step2_ocr"
sys.path.append(step2_folder)
from step2_ocr_paddle import run_ocr

# =====================================================
# STEP 3 IMPORT
# =====================================================
step3_folder = r"C:\ocr-pipeline\step3_lightclean"
sys.path.append(step3_folder)
from step3_light_clean import clean_ocr_json

# =====================================================
# BATCH PIPELINE
# =====================================================
for pdf_path in CV_INPUT_DIR.glob("*.pdf"):
    cv_name = pdf_path.stem
    print(f"\n=== Processing CV: {cv_name} ===")

    # Per-CV folders
    step1_out = BASE_STEP1_OUT / cv_name
    step2_out = BASE_STEP2_OUT / cv_name
    step3_out = BASE_STEP3_OUT / cv_name
    step3_out.mkdir(parents=True, exist_ok=True)

    # -------------------------------
    # Step 1: PDF → PNG
    # -------------------------------
    try:
        preprocess_pdf(
            str(pdf_path),
            str(step1_out),
            poppler_path=POPPLER_PATH
        )
    except Exception as e:
        print(f"[ERROR] Step 1 failed for {cv_name}: {e}")
        continue

    # -------------------------------
    # Step 2: OCR
    # -------------------------------
    try:
        run_ocr(
            str(step1_out),
            str(step2_out)
        )
    except Exception as e:
        print(f"[ERROR] Step 2 failed for {cv_name}: {e}")
        continue

    # -------------------------------
    # Step 3: Light Clean
    # -------------------------------
    raw_json = step2_out / "cv_ocr_raw.json"
    clean_json = step3_out / "cv_ocr_cleaned.json"

    if not raw_json.exists():
        print(f"[SKIP] No OCR output for {cv_name}")
        continue

    try:
        clean_ocr_json(
            str(raw_json),
            str(clean_json)
        )
    except Exception as e:
        print(f"[ERROR] Step 3 failed for {cv_name}: {e}")
        continue

    print(f"[DONE] {cv_name}")
