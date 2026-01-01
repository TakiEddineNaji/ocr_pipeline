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