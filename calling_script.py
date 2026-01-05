import sys
from pathlib import Path

# -------------------------------
# Step 1: Preprocess PDF → PNG images
# -------------------------------
step1_folder = r"C:\ocr-pipeline\step1_preprocess"
sys.path.append(step1_folder)

from step1_preprocess_pdf import main as preprocess_pdf

preprocess_pdf(
    r"C:\ocr-pipeline\step1_preprocess\cv.pdf",
    r"C:\ocr-pipeline\step1_preprocess\step1_output",
    poppler_path=r"C:\poppler\Library\bin"
)

# -------------------------------
# Step 2: OCR on processed images
# -------------------------------
step2_folder = r"C:\ocr-pipeline\step2_ocr"
sys.path.append(step2_folder)

from step2_ocr_paddle import run_ocr  # import the function

run_ocr(
    r"C:\ocr-pipeline\step1_preprocess\step1_output",
    r"C:\ocr-pipeline\step2_ocr\step2_output"
)

# -------------------------------
# Step 3: Light cleaning OCR results
# -------------------------------
step3_folder = r"C:\ocr-pipeline\step3_lightclean"
sys.path.append(step3_folder)
from step3_light_clean import clean_ocr_json

clean_ocr_json(
    r"C:\ocr-pipeline\step2_ocr\step2_output\cv_ocr_raw.json",
    r"C:\ocr-pipeline\step3_lightclean\step3_output\cv_ocr_cleaned.json"
)

# =====================================================
# STEP 4 — RAG PREPARATION (BLOCK BUILDING)
# =====================================================

step4_folder = r"C:\ocr-pipeline\step4_rag"
sys.path.append(step4_folder)

from step4_rag_prepare import main as prepare_rag_blocks

prepare_rag_blocks(
    r"C:\ocr-pipeline\step3_lightclean\step3_output\cv_ocr_cleaned.json",
    r"C:\ocr-pipeline\step4_rag\step4_output\cv_rag_blocks.json",
    "cv_001"
)

# =====================================================
# Step 5: Embeddings
# =====================================================
step5_folder = r"C:\ocr-pipeline\step5_embeddings"
sys.path.append(step5_folder)

from step5_embeddings import main as build_embeddings

build_embeddings(
    r"C:\ocr-pipeline\step4_rag\step4_output\cv_rag_blocks.json",
    r"C:\ocr-pipeline\step5_embeddings\step5_output"
)

# =====================================================
# Step 6: Retrieval (Chroma)
# =====================================================
step6_folder = r"C:\ocr-pipeline\step6_retrieval"
sys.path.append(step6_folder)

from step6_retrieval import main as retrieve_blocks

retrieve_blocks(
    r"C:\ocr-pipeline\step5_embeddings\step5_output",
    "What experience does the candidate have in data science?",
    3
)