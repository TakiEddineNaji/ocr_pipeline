Automated CV Intelligence System  
Local OCR + RAG Pipeline for Skill Extraction and Labor-Market Analysis

---

TL;DR

A fully local, deterministic OCR pipeline for CVs, extended with embedding-based  
semantic retrieval and multi-candidate Retrieval-Augmented Generation (RAG) to enable  
grounded, searchable document understanding — without cloud dependencies.

---

Development Environment

The project is currently developed and tested on Windows.  
A Linux (Ubuntu) environment is planned for future versions to support  
GPU-accelerated OCR, embeddings, and local LLM inference.

---

Overview

This project implements a production-oriented pipeline that converts CVs  
(PDF, PNG, JPEG, JPG) into structured, searchable knowledge using OCR,  
deterministic text cleaning, embeddings, semantic retrieval, and  
retrieval-augmented LLMs.

The system is designed to be offline-first, modular, and automation-ready.  
Its goal is not free-form text generation, but reliable document understanding  
and retrieval as a foundation for automated CV intelligence and labor-market  
analysis.

---

Why This Project Exists

Most CV processing systems today are either:
- Cloud-dependent and opaque
- Script-based OCR pipelines without retrieval guarantees
- End-to-end ML systems that mix extraction, interpretation, and scoring

This project explores a different approach:
- Fully local execution (OCR, embeddings, retrieval, LLM)
- Deterministic preprocessing and cleaning
- Embedding-based semantic retrieval
- Retrieval-Augmented Generation (RAG), not hallucination-prone generation
- Clear separation between extraction, retrieval, aggregation, and reasoning

---

High-Level Architecture (Actual Implementation)

PDF CV  
→ Step 1: PDF / Image Preprocessing  
→ Step 2: OCR (PaddleOCR)  
→ Step 3: Light OCR Cleaning (No Semantics)  
→ Step 4: RAG Block Preparation (Paragraph-Level Text)  
→ Step 5: Shared Embeddings + Vector Store (Chroma)  
→ Step 6: Semantic Retrieval + Candidate Aggregation  
→ Step 7: LLM Answering (Multi-Candidate RAG)

---

Core RAG Flow

Knowledge is built once:
- OCR text is cleaned deterministically
- Cleaned text is converted into dense RAG blocks
- RAG blocks are embedded using a pre-trained embedding model
- All CVs are embedded into a single shared vector database
- Each block has a unique ID based on CV name, page, and block index

At query time:
Question  
→ Retrieve relevant blocks (Step 6)  
→ Group blocks by candidate (CV)  
→ LLM reasons per candidate using retrieved context only (Step 7)

---

Core Design Principles

- Fully local execution
- Deterministic preprocessing
- JSON as canonical intermediate format
- Retrieval first, generation second
- Candidate-level reasoning via aggregation
- Idempotent embeddings (safe re-runs)
- Offline-first, production-oriented design

---

Folder Structure

ocr-pipeline/
├── step1_preprocess/
│   └── step1_preprocess_pdf.py
├── step2_ocr/
│   └── step2_ocr_paddle.py
├── step3_lightclean/
│   └── step3_light_clean.py
├── step4_rag/
│   └── step4_rag_prepare.py
├── step5_embeddings/
│   ├── step5_embeddings.py
│   └── step5_output/        (shared Chroma DB)
├── step6_retrieval/
│   └── step6_retrieval.py
├── step7_llm/
│   └── step7_llm_answering.py
└── caller_batch/
    └── cvs_input
    └── step1_batch_output
    └── step3_batch_output
    └── step4_batch_output
    └── step5_batch_output
    └── caller_batch.py
---

Pipeline Stages

Step 1 — Preprocessing  
Convert PDFs and images into normalized PNG pages.

Step 2 — OCR  
Extract raw text and layout metadata using PaddleOCR.

Step 3 — Light Cleaning  
Deterministic cleanup only (no semantics, no LLM).

Step 4 — RAG Block Preparation  
Merge OCR lines into paragraph-level blocks.

Step 5 — Embeddings  
Embed all CV blocks into a single shared Chroma vector database.

Step 6 — Retrieval + Aggregation  
Retrieve relevant blocks and group them by candidate (CV ID).

Step 7 — LLM Answering  
LLM reasons per candidate using retrieved context only.

---

Example Query

Query:  
Which candidates have a master degree and are under 30?

Answer:
Candidates cv2 and cv4 meet the criteria.

---

Final Notes

This project is intentionally:
- Offline-first
- Deterministic
- Retrieval-driven
- Candidate-aware
- Production-oriented
