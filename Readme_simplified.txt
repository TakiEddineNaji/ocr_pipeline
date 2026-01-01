
CV OCR PIPELINE — FULL DOCUMENTATION (STEP 1 → STEP 3)

1. OVERVIEW
This project implements a 3-step OCR pipeline for CV processing:
- Step 1: PDF preprocessing (PDF → images)
- Step 2: OCR using PaddleOCR (images → raw JSON)
- Step 3: Light cleaning (raw JSON → cleaned JSON, pre-LLM)

The pipeline is designed for batch processing and modular execution.
Core scripts never change; only caller scripts do.

2. FOLDER STRUCTURE

C:\ocr-pipeline\
│
├── step1_preprocess\
│   ├── step1_preprocess.py
│   └── step1_output\
│
├── step2_ocr\
│   ├── step2_ocr_paddle.py
│   └── step2_output\
│
├── step3_lightclean\
│   ├── step3_light_clean.py
│   └── step3_output\
│
├── callers\
│   ├── run_step1.py
│   ├── run_step2.py
│   └── run_step3.py
│
└── cvs\
    └── input_pdfs\

3. STEP 1 — PREPROCESSING
Input: PDF CVs
Output: processed PNG images
Purpose:
- Convert PDFs to images
- Normalize DPI
- Prepare clean input for OCR

4. STEP 2 — OCR
Input: Images from Step 1
Output: Raw OCR JSON
JSON is used because it preserves:
- Bounding boxes
- Confidence scores
- Layout order

5. STEP 3 — LIGHT CLEANING
Input: Raw OCR JSON
Output: Cleaned OCR JSON

Cleaning includes:
- Removing low-confidence lines
- Normalizing whitespace
- Removing accents (unidecode)
- Preserving layout order

No semantic interpretation is performed.

6. BATCH PROCESSING
Each step supports batch execution.
Caller scripts loop over folders and invoke core scripts.

7. EXECUTION MODES
Each step can be:
- Run as a CLI script
- Imported and called as a Python function
- Orchestrated via subprocess using a specific virtual environment

8. RECOMMENDED FORMAT
JSON is preferred over TXT/MD because:
- It is structured
- It is machine-readable
- It preserves OCR metadata
- It is LLM-ready

TXT or MD can be generated later AFTER semantic processing.

END OF DOCUMENTATION
