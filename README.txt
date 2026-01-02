# CV OCR Pipeline — Local, Modular, RAG-Ready

## Overview

This project implements a fully local, production-oriented CV processing pipeline that converts PDF CVs into searchable, structured knowledge using OCR, deterministic cleaning, embeddings, and LLM-powered retrieval (RAG).

The system is offline-first, modular, and designed for automation and scaling without relying on cloud OCR or hosted LLMs.

---

## High-Level Architecture

PDF CV  
→ Step 1: PDF → PNG Preprocessing  
→ Step 2: OCR (PaddleOCR, GPU)  
→ Step 3: Light OCR Cleaning (No Semantics)  
→ Step 4: RAG Ingestion & Embeddings  
→ Step 5: LLM + Frontend Interaction  

---

## Key Design Principles

- Fully local execution (OCR, embeddings, LLM)
- Deterministic preprocessing and cleaning
- JSON as the canonical intermediate format
- Retrieval-Augmented Generation (RAG), not free generation
- Clear separation between extraction, cleaning, retrieval, and interaction

---

## Folder Structure

ocr-pipeline/
├── step1_preprocess/
│ ├── step1_preprocess_pdf.py
│ └── output/
├── step2_ocr/
│ ├── step2_ocr_paddle.py
│ └── output/
│ └── cv_ocr_raw.json
├── step3_lightclean/
│ ├── step3_light_clean.py
│ └── output/
│ └── cv_ocr_cleaned.json
├── step4_rag/
│ ├── ingest_embeddings.py
│ ├── vector_store/
│ └── metadata/
├── step5_frontend/
│ ├── api_server.py
│ └── ui/
└── callers/
├── run_step2_subprocess.py
└── run_step3_subprocess.py


---

## Step 1 — PDF Preprocessing

Purpose:
- Convert PDF pages to normalized PNG images
- Preserve page order and resolution

Input:
- PDF CV

Output:
- processed_*.png

CLI:


---

## Step 2 — OCR (PaddleOCR)

Purpose:
- Extract raw text from images
- Preserve layout, confidence scores, and page structure

Input:
- PNG images

Output:
- cv_ocr_raw.json

CLI:


---

## Step 3 — Light OCR Cleaning (Pre-RAG)

Purpose:
- Prepare OCR text for embeddings without semantic interpretation

Operations:
- Remove low-confidence lines
- Normalize whitespace and casing
- Normalize accents
- Preserve reading order

Input:
- cv_ocr_raw.json

Output:
- cv_ocr_cleaned.json

CLI:


---

## Step 4 — RAG Ingestion & Embeddings

Purpose:
- Convert cleaned OCR text into searchable vectors

Operations:
- Chunk text by page or logical blocks
- Generate embeddings locally
- Store vectors in a vector database
- Attach metadata (CV ID, page, section hints)

Output:
- Persistent vector store

---

## Step 5 — LLM + Frontend Interaction

Purpose:
- Natural language interaction with CV data
- All responses are grounded via retrieval

Components:
- Backend API (e.g., FastAPI)
- Vector search (FAISS / Chroma)
- Local LLM (llama.cpp)
- Optional web frontend

---

## Automation Strategy

- Each step is stateless and callable
- Batch processing is handled by caller scripts
- Easy to debug, automate, and scale

---

## Final Notes

This pipeline is intentionally:
- Offline-first
- Modular
- Deterministic
- RAG-driven
- Production-oriented

End of README.
