CV OCR PIPELINE — TECHNICAL README
=================================

This document describes the full technical implementation of the CV OCR pipeline,
including callable modules, CLI execution, batch processing, and environment isolation.

--------------------------------------------------
1. OVERALL ARCHITECTURE
--------------------------------------------------

The pipeline is intentionally split into independent, stateless steps:

STEP 1: PDF → PNG preprocessing
STEP 2: OCR on PNG images (PaddleOCR)
STEP 3: Light OCR cleaning (pre-LLM)

Each step:
- Can be called as a Python function
- Can be executed as a standalone CLI script
- Can be orchestrated via subprocess using a specific virtual environment
- Produces deterministic outputs consumed by the next step

No step depends on global state or hardcoded paths.

--------------------------------------------------
2. FOLDER STRUCTURE
--------------------------------------------------

C:\ocr-pipeline\
│
├── step1_preprocess\
│   ├── step1_preprocess_pdf.py
│   ├── cv.pdf
│   └── step1_output\
│       └── processed_1.png ...
│
├── step2_ocr\
│   ├── step2_ocr_paddle.py
│   └── step2_output\
│       └── cv_ocr_raw.json
│
├── step3_lightclean\
│   ├── step3_light_clean.py
│   └── step3_output\
│       └── cv_ocr_cleaned.json
│
└── callers\
    ├── run_step2_subprocess.py
    └── run_step3_subprocess.py

--------------------------------------------------
3. STEP 1 — PDF PREPROCESSING
--------------------------------------------------

File:
step1_preprocess_pdf.py

Callable entry:
main(pdf_path, output_dir, poppler_path)

Responsibilities:
- Convert PDF pages to images
- Normalize DPI and format
- Preserve page order
- Output processed_*.png

External dependency:
- Poppler (explicit path passed as argument)

CLI usage:
python step1_preprocess_pdf.py input.pdf output_folder poppler_path

--------------------------------------------------
4. STEP 2 — OCR (PADDLEOCR)
--------------------------------------------------

File:
step2_ocr_paddle.py

Callable entry:
run_ocr(input_dir, output_dir)

Responsibilities:
- Load processed_*.png
- Run PaddleOCR
- Normalize OCR formats (new + legacy)
- Save raw OCR output to JSON

Output format:
cv_ocr_raw.json

Design note:
JSON is used instead of TXT/MD to preserve:
- Confidence scores
- Bounding boxes
- Page structure
- Machine-readability for later LLM usage

CLI usage:
python step2_ocr_paddle.py input_folder output_folder

--------------------------------------------------
5. STEP 3 — LIGHT OCR CLEANING
--------------------------------------------------

File:
step3_light_clean.py

Callable entry:
clean_ocr_json(input_json, output_json)

Responsibilities:
- Remove low-confidence OCR lines
- Normalize whitespace
- Remove accents (unidecode)
- Preserve reading order when bbox exists
- Produce clean but non-semantic text

Important:
Bounding boxes may be None.
Sorting logic must handle None safely.

CLI usage:
python step3_light_clean.py raw.json cleaned.json

--------------------------------------------------
6. BATCH PROCESSING STRATEGY
--------------------------------------------------

Batching is handled ONLY in caller scripts.

Source scripts remain unchanged.

Example:
- Loop over multiple PDFs
- For each PDF:
  - Create isolated output folders
  - Call step 1
  - Call step 2
  - Call step 3

This ensures:
- Reproducibility
- Easier debugging
- Parallelization later

--------------------------------------------------
7. VENV ISOLATION WITH SUBPROCESS
--------------------------------------------------

Heavy dependencies (PaddleOCR) are isolated in a venv.

Caller script example:

subprocess.run(
    [venv_python, step2_script, input_dir, output_dir],
    capture_output=True,
    text=True
)

This guarantees:
- Correct dependency versions
- No global Python pollution
- Production-grade execution

--------------------------------------------------
8. WHY JSON (NOT TXT / MD)
--------------------------------------------------

TXT / MD:
- Human-readable
- Loses structure
- Loses confidence
- Hard to post-process

JSON:
- Machine-readable
- Structured
- LLM-friendly
- Auditable

JSON is the correct intermediate format.
TXT / MD are final presentation formats only.

--------------------------------------------------
9. COMMON PITFALLS
--------------------------------------------------

- sys.path must point to the folder, not the file
- Module name == filename (without .py)
- Import errors ≠ code errors (they are path errors)
- __pycache__ is normal (compiled bytecode)
- None bbox must be handled before sorting

--------------------------------------------------
10. FINAL NOTE
--------------------------------------------------

This pipeline is intentionally:
- Modular
- Explicit
- Debuggable
- Production-oriented

You now have:
- OCR extraction
- Deterministic cleaning
- LLM-ready structured data

End of technical README.
